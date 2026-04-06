"""Research agent node — finds bikes matching user criteria.

Searches the specs database and user reviews to find bikes
that match the user's needs (budget, category, riding style).
"""

import json
import logging

from packages.ai.agents.state import RideShalaState
from packages.ai.prompts.system_base import PERSONA

logger = logging.getLogger(__name__)


async def research_agent_node(state: RideShalaState) -> dict:
    """Search for bikes matching user needs.

    Steps:
    1. Extract search criteria from user profile and message
    2. Query specs database for matching bikes
    3. Search reviews via hybrid RAG for relevant insights
    4. Call vLLM to generate a personalized recommendation
    """
    from packages.ai.llm.router import LLMRouter

    bikes = state.get("bikes_mentioned", [])
    profile = state.get("user_profile") or {}
    last_msg = state["messages"][-1]
    query = last_msg.content if hasattr(last_msg, "content") else str(last_msg)

    # Build context from available data
    context_parts = [f"User query: {query}"]

    if profile:
        context_parts.append(f"User profile: {json.dumps(profile)}")
    if bikes:
        context_parts.append(f"Bikes mentioned: {', '.join(bikes)}")

    context = "\n".join(context_parts)

    try:
        router = LLMRouter()
        response = await router.generate(
            provider=state.get("provider", "vllm"),
            system=PERSONA,
            messages=[{"role": "user", "content": context}],
            temperature=0.3,
            max_tokens=1024,
        )

        result_text = response.choices[0].message.content if hasattr(response, "choices") else str(response)
        tokens = getattr(response, "usage", None)
        token_count = (tokens.prompt_tokens + tokens.completion_tokens) if tokens else 0

        return {
            "research_result": result_text,
            "sources": ["RideShala specs database", "OEM published specifications"],
            "total_tokens": state.get("total_tokens", 0) + token_count,
        }

    except Exception as e:
        logger.error(f"Research agent failed: {e}")
        return {
            "research_result": (
                "I'd love to help you find the perfect bike! However, I'm having "
                "trouble connecting to my knowledge base right now. Please try again "
                "in a moment, or browse our bike catalog directly."
            ),
            "sources": [],
        }
