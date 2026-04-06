"""Synthesize node — combines agent outputs into a coherent response."""

from packages.ai.agents.state import RideShalaState


async def synthesize_node(state: RideShalaState) -> dict:
    """Combine all agent outputs into a single response with citations.

    Merges results from whichever agents ran, formats with sources,
    and prepares the final response for the guardrail check.
    """
    parts = []
    sources = list(state.get("sources", []))

    for key in ["research_result", "comparison_result", "safety_result", "finance_result", "ride_plan_result"]:
        result = state.get(key)
        if result:
            parts.append(result)

    if not parts:
        # General chat — no agent ran, generate conversational response
        # TODO: Call LLM for general chat
        parts.append("How can I help you find the perfect bike today?")

    combined = "\n\n".join(parts)

    # Add source citations footer if any
    if sources:
        combined += "\n\n---\n**Sources:** " + " | ".join(sources)

    return {
        "messages": [{"role": "assistant", "content": combined}],
        "sources": sources,
    }
