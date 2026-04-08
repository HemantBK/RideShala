"""Research agent node — finds bikes matching user criteria.

Queries the REAL specs database and user reviews to find bikes
that match the user's needs (budget, category, riding style).
Passes real data to the LLM for personalized recommendations.
"""

import json
import logging

from packages.ai.agents.state import RideShalaState
from packages.ai.prompts.system_base import PERSONA

logger = logging.getLogger(__name__)


async def research_agent_node(state: RideShalaState) -> dict:
    """Search for bikes matching user needs using real database data.

    Steps:
    1. Extract search criteria from user profile
    2. Query specs database for matching bikes
    3. Format real spec data as LLM context
    4. Call LLM to generate personalized recommendation with citations
    """
    from packages.ai.agents.tools.search_specs import search_bike_specs
    from packages.ai.llm.router import LLMRouter

    bikes = state.get("bikes_mentioned", [])
    profile = state.get("user_profile") or {}
    last_msg = state["messages"][-1]
    query = last_msg.content if hasattr(last_msg, "content") else str(last_msg)

    # 1. Query real specs database
    matched_bikes = []

    if bikes:
        # Search for specifically mentioned bikes
        for bike_name in bikes:
            results = await search_bike_specs(model_name=bike_name)
            matched_bikes.extend(results)
    else:
        # Search by profile criteria
        results = await search_bike_specs(
            category=profile.get("riding_style"),
            max_price=profile.get("budget_inr"),
        )
        matched_bikes = results[:10]  # Top 10 matches

    # 2. Build context with REAL data
    context_parts = [f"User query: {query}"]

    if profile:
        context_parts.append(f"User profile: {json.dumps(profile)}")

    if matched_bikes:
        context_parts.append(f"\n--- REAL BIKE DATA FROM OUR DATABASE ({len(matched_bikes)} matches) ---")
        for bike in matched_bikes[:8]:
            specs_text = (
                f"\n{bike['brand']} {bike['name']} ({bike.get('engine_cc', '?')}cc):\n"
                f"  Price: Rs {bike.get('price_ex_showroom_inr', 'N/A'):,} ex-showroom\n"
                f"  Power: {bike.get('power_bhp', '?')} bhp | Torque: {bike.get('torque_nm', '?')} Nm\n"
                f"  Weight: {bike.get('weight_kg', '?')} kg | Seat: {bike.get('seat_height_mm', '?')}mm\n"
                f"  Tank: {bike.get('fuel_tank_litres', '?')}L | Mileage: {bike.get('mileage_claimed_kpl', '?')} kpl (claimed)\n"
                f"  ABS: {bike.get('abs_type', 'unknown')} | TC: {bike.get('traction_control', False)}\n"
                f"  [Source: {bike.get('source_url', 'OEM website')}]"
            )
            context_parts.append(specs_text)
    else:
        context_parts.append(
            "No exact matches found in our database. Use your general knowledge "
            "but clearly state that these specs should be verified on the OEM website."
        )

    # 3. Try to get review data via hybrid RAG
    review_context = ""
    try:
        from packages.ai.rag.hybrid_search import HybridRAG

        rag = HybridRAG()
        review_results = await rag.search(query=query, top_k=5)
        if review_results:
            review_context = "\n--- USER REVIEWS FROM RIDESHALA ---\n"
            for r in review_results:
                review_context += f"- \"{r['text'][:200]}...\" (rating context, {r['source']})\n"
            context_parts.append(review_context)
    except Exception as e:
        logger.debug(f"RAG search unavailable (expected during MVP): {e}")

    context = "\n".join(context_parts)

    # 4. Call LLM with real data
    try:
        router = LLMRouter()
        best_provider = await router.get_provider_for_task("research")
        logger.info(f"research_agent_calling_llm provider={best_provider} context_length={len(context)}")
        response = await router.generate(
            provider=best_provider,
            system=PERSONA,
            messages=[{"role": "user", "content": context}],
            temperature=0.3,
            max_tokens=1024,
        )

        result_text = response.choices[0].message.content if hasattr(response, "choices") else str(response)
        tokens = getattr(response, "usage", None)
        token_count = (tokens.prompt_tokens + tokens.completion_tokens) if tokens else 0

        # Build source list from actual data used
        sources = []
        for bike in matched_bikes[:5]:
            sources.append(f"{bike['brand']} {bike['name']} specs from {bike.get('source_url', 'OEM website')}")
        if review_context:
            sources.append("User reviews from RideShala community")

        return {
            "research_result": result_text,
            "specs_data": {b["slug"]: b for b in matched_bikes[:5]},
            "sources": sources,
            "total_tokens": state.get("total_tokens", 0) + token_count,
        }

    except Exception as e:
        logger.error(f"Research agent LLM failed: {type(e).__name__}: {e}")
        # Fallback: return raw spec data without LLM
        if matched_bikes:
            fallback = "Here are the bikes I found in our database:\n\n"
            for bike in matched_bikes[:5]:
                fallback += (
                    f"**{bike['brand']} {bike['name']}** — Rs {bike.get('price_ex_showroom_inr', 'N/A'):,}\n"
                    f"  {bike.get('engine_cc', '?')}cc | {bike.get('power_bhp', '?')} bhp | "
                    f"{bike.get('seat_height_mm', '?')}mm seat | {bike.get('abs_type', '?')} ABS\n\n"
                )
            fallback += "_AI reasoning unavailable right now. Try again in a moment._"
            return {"research_result": fallback, "sources": ["RideShala specs database"]}

        return {
            "research_result": "I couldn't find matching bikes right now. Please try again.",
            "sources": [],
        }
