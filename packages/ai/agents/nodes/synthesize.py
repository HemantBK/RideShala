"""Synthesize node — combines agent outputs into a coherent response.

When specific agents ran, merges their outputs with citations.
When no agent ran (general chat), calls the LLM for a conversational response.
"""

import logging

from packages.ai.agents.state import RideShalaState
from packages.ai.prompts.system_base import PERSONA

logger = logging.getLogger(__name__)


async def synthesize_node(state: RideShalaState) -> dict:
    """Combine all agent outputs into a single response with citations."""
    parts = []
    sources = list(state.get("sources", []))

    for key in [
        "research_result",
        "comparison_result",
        "safety_result",
        "finance_result",
        "ride_plan_result",
    ]:
        result = state.get(key)
        if result:
            parts.append(result)

    if not parts:
        # General chat — call LLM for a conversational response
        last_msg = state["messages"][-1]
        query = last_msg.content if hasattr(last_msg, "content") else str(last_msg)

        try:
            from packages.ai.llm.router import LLMRouter

            router = LLMRouter()
            best_provider = await router.get_provider_for_task("chat")
            response = await router.generate(
                provider=best_provider,
                system=PERSONA,
                messages=[{"role": "user", "content": query}],
                temperature=0.7,
                max_tokens=512,
            )

            if hasattr(response, "choices"):
                parts.append(response.choices[0].message.content)
            else:
                parts.append(str(response))

        except Exception as e:
            logger.debug(f"LLM unavailable for general chat: {e}")
            parts.append(
                "Welcome to RideShala! I'm your AI motorcycle advisor. "
                "Tell me about yourself — height, budget, city, riding style — "
                "and I'll find the perfect bike for you. You can also ask me to "
                "compare bikes, check safety features, or calculate ownership costs."
            )

    combined = "\n\n".join(parts)

    # Add source citations footer
    if sources:
        combined += "\n\n---\n**Sources:** " + " | ".join(sources)

    return {
        "messages": [{"role": "assistant", "content": combined}],
        "sources": sources,
        "total_tokens": state.get("total_tokens", 0),
    }
