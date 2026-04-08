"""Comparison agent node — detailed bike comparison with reasoning.

Fetches REAL specs from the database and passes them to the LLM
for nuanced trade-off analysis. Falls back to vLLM by default (free).
"""

import json
import logging

from packages.ai.agents.state import RideShalaState
from packages.ai.prompts.system_base import COMPARISON_PROMPT, PERSONA

logger = logging.getLogger(__name__)


async def comparison_agent_node(state: RideShalaState) -> dict:
    """Compare bikes using real database specs + LLM reasoning.

    Steps:
    1. Fetch real specs for all mentioned bikes from database
    2. Try to fetch relevant reviews via hybrid RAG
    3. Build rich context with real data
    4. Call LLM for reasoned comparison with citations
    """
    from packages.ai.agents.tools.search_specs import search_bike_specs
    from packages.ai.llm.router import LLMRouter

    bikes = state.get("bikes_mentioned", [])
    profile = state.get("user_profile") or {}

    if len(bikes) < 2:
        return {
            "comparison_result": "Please mention at least 2 bikes to compare. "
            "For example: 'Compare Meteor 350 vs CB350'",
            "sources": [],
        }

    # 1. Fetch REAL specs for each bike
    specs = {}
    sources = []
    for bike_name in bikes:
        results = await search_bike_specs(model_name=bike_name)
        if results:
            specs[bike_name] = results[0]
            sources.append(
                f"{results[0]['brand']} {results[0]['name']} specs from "
                f"{results[0].get('source_url', 'OEM website')}"
            )

    # 2. Build comparison context with REAL data
    context_parts = [f"Compare these motorcycles: {', '.join(bikes)}"]

    if profile:
        context_parts.append(f"User profile: {json.dumps(profile)}")

    if specs:
        context_parts.append("\n--- REAL SPECS FROM OUR DATABASE ---")
        for name, spec in specs.items():
            context_parts.append(
                f"\n**{spec['brand']} {spec['name']}**\n"
                f"  Engine: {spec.get('engine_cc', '?')}cc, {spec.get('power_bhp', '?')} bhp, "
                f"{spec.get('torque_nm', '?')} Nm\n"
                f"  Weight: {spec.get('weight_kg', '?')} kg\n"
                f"  Seat height: {spec.get('seat_height_mm', '?')}mm\n"
                f"  Tank: {spec.get('fuel_tank_litres', '?')}L\n"
                f"  ABS: {spec.get('abs_type', 'unknown')} | "
                f"Traction control: {spec.get('traction_control', False)}\n"
                f"  Mileage (claimed): {spec.get('mileage_claimed_kpl', '?')} kpl\n"
                f"  Price: Rs {spec.get('price_ex_showroom_inr', 'N/A'):,} ex-showroom\n"
                f"  Gears: {spec.get('gears', '?')} | Cooling: {spec.get('cooling', '?')}\n"
                f"  [Source: {spec.get('source_url', 'OEM website')}]"
            )
    else:
        context_parts.append(
            "Could not find these bikes in our database. Use general knowledge "
            "but state clearly that specs should be verified on OEM websites."
        )

    # 3. Try to fetch reviews via RAG
    try:
        from packages.ai.rag.hybrid_search import HybridRAG

        rag = HybridRAG()
        for bike_name in bikes[:3]:
            reviews = await rag.search(query=f"{bike_name} ownership experience", bike_model=bike_name, top_k=3)
            if reviews:
                context_parts.append(f"\n--- USER REVIEWS: {bike_name} ---")
                for r in reviews:
                    context_parts.append(f"- \"{r['text'][:200]}\" [{r['source']}]")
                sources.append(f"{bike_name} reviews from RideShala community")
    except Exception as e:
        logger.debug(f"RAG unavailable for comparison (expected during MVP): {e}")

    context = "\n\n".join(context_parts)
    system = f"{PERSONA}\n\n{COMPARISON_PROMPT}"

    # 4. Call LLM with real data
    try:
        router = LLMRouter()
        response = await router.generate(
            provider=state.get("provider", "vllm"),
            system=system,
            messages=[{"role": "user", "content": context}],
            temperature=0.3,
            max_tokens=2048,
        )

        if hasattr(response, "choices"):
            result_text = response.choices[0].message.content
        elif hasattr(response, "content"):
            result_text = (
                response.content[0].text
                if isinstance(response.content, list)
                else str(response.content)
            )
        else:
            result_text = str(response)

        tokens = getattr(response, "usage", None)
        token_count = 0
        if tokens:
            token_count = getattr(tokens, "prompt_tokens", 0) + getattr(tokens, "completion_tokens", 0)

        return {
            "comparison_result": result_text,
            "specs_data": specs,
            "sources": sources,
            "total_tokens": state.get("total_tokens", 0) + token_count,
        }

    except Exception as e:
        logger.error(f"Comparison agent failed: {e}")
        # Fallback: return raw specs side-by-side without LLM
        if specs:
            fallback = "**Quick Spec Comparison** (AI reasoning unavailable):\n\n"
            fallback += "| Spec | " + " | ".join(bikes) + " |\n"
            fallback += "|---|" + "|".join(["---"] * len(bikes)) + "|\n"
            for field, label in [
                ("price_ex_showroom_inr", "Price"),
                ("engine_cc", "Engine"),
                ("power_bhp", "Power"),
                ("seat_height_mm", "Seat"),
                ("weight_kg", "Weight"),
                ("abs_type", "ABS"),
            ]:
                row = f"| {label} | "
                for name in bikes:
                    val = specs.get(name, {}).get(field, "N/A")
                    if field == "price_ex_showroom_inr" and isinstance(val, int):
                        val = f"Rs {val:,}"
                    row += f"{val} | "
                fallback += row + "\n"
            return {"comparison_result": fallback, "specs_data": specs, "sources": sources}

        return {
            "comparison_result": f"Could not compare {' vs '.join(bikes)} right now.",
            "sources": [],
        }
