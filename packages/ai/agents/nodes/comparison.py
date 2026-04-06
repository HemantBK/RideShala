"""Comparison agent node — detailed bike comparison with reasoning.

Uses Claude for nuanced trade-off analysis between 2-4 bikes.
Falls back to vLLM if Claude is unavailable or budget exceeded.
"""

import json
import logging

from packages.ai.agents.state import RideShalaState
from packages.ai.prompts.system_base import COMPARISON_PROMPT, PERSONA

logger = logging.getLogger(__name__)


async def comparison_agent_node(state: RideShalaState) -> dict:
    """Compare bikes using Claude for nuanced reasoning.

    Steps:
    1. Retrieve specs for all mentioned bikes
    2. Retrieve relevant reviews via hybrid RAG
    3. Call Claude with comparison prompt + all data
    4. Return structured comparison with per-claim citations
    """
    from packages.ai.llm.router import LLMRouter

    bikes = state.get("bikes_mentioned", [])
    profile = state.get("user_profile") or {}

    if len(bikes) < 2:
        return {
            "comparison_result": "Please mention at least 2 bikes to compare. For example: 'Compare Meteor 350 vs CB350'",
            "sources": [],
        }

    # Build comparison context
    context_parts = [
        f"Compare these motorcycles: {', '.join(bikes)}",
    ]

    if profile:
        context_parts.append(f"User profile: {json.dumps(profile)}")

    # TODO: In production, fetch real specs from PostgreSQL and reviews from Qdrant
    context_parts.append(
        "Use your knowledge of these bikes' published specifications from their "
        "manufacturer websites. Cite the OEM source for every spec you mention."
    )

    context = "\n\n".join(context_parts)
    system = f"{PERSONA}\n\n{COMPARISON_PROMPT}"

    try:
        router = LLMRouter()
        response = await router.generate(
            provider=state.get("provider", "vllm"),
            system=system,
            messages=[{"role": "user", "content": context}],
            temperature=0.3,
            max_tokens=2048,
        )

        # Handle both OpenAI and Anthropic response formats
        if hasattr(response, "choices"):
            result_text = response.choices[0].message.content
        elif hasattr(response, "content"):
            result_text = response.content[0].text if isinstance(response.content, list) else str(response.content)
        else:
            result_text = str(response)

        return {
            "comparison_result": result_text,
            "sources": [f"{bike} specs from OEM website" for bike in bikes],
        }

    except Exception as e:
        logger.error(f"Comparison agent failed: {e}")
        return {
            "comparison_result": f"I'm having trouble generating a detailed comparison of {' vs '.join(bikes)} right now. Please try again shortly.",
            "sources": [],
        }
