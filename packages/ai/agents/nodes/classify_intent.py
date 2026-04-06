"""Intent classification node — routes queries to the right agent.

Uses vLLM (free, self-hosted) to classify user intent and extract entities.
Low-confidence results trigger the clarification flow.
All processing uses the free self-hosted model by default.
"""

import json
import logging

from packages.ai.agents.state import RideShalaState

logger = logging.getLogger(__name__)


async def classify_intent_node(state: RideShalaState) -> dict:
    """Classify the user's intent using vLLM (fast, free).

    Returns:
        Updated state with intent, bikes_mentioned, user_profile, and provider.
    """
    from packages.ai.llm.router import LLMRouter
    from packages.ai.prompts.system_base import INTENT_CLASSIFICATION_PROMPT

    last_message = state["messages"][-1]
    content = last_message.content if hasattr(last_message, "content") else str(last_message)

    router = LLMRouter()

    try:
        response = await router.generate(
            provider="vllm",
            system=INTENT_CLASSIFICATION_PROMPT,
            messages=[{"role": "user", "content": content}],
            temperature=0.1,
            max_tokens=256,
        )

        result_text = response.choices[0].message.content
        result = json.loads(result_text)

        confidence = result.get("confidence", 0.0)
        intent = result.get("intent", "general_chat")

        # Low confidence -> ask for clarification
        if confidence <= 0.6:
            intent = "clarify"

        # Determine best provider for this intent
        provider = await router.get_provider_for_task(intent)

        return {
            "intent": intent,
            "bikes_mentioned": result.get("bikes", []),
            "user_profile": result.get("profile"),
            "needs_clarification": confidence <= 0.6,
            "provider": provider,
        }

    except Exception as e:
        logger.error(f"Intent classification failed: {e}")
        return {
            "intent": "general_chat",
            "bikes_mentioned": [],
            "needs_clarification": False,
            "provider": "vllm",
        }
