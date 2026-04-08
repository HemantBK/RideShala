"""Intent classification node — routes queries to the right agent.

Uses the best available LLM to classify user intent and extract entities.
Low-confidence results trigger the clarification flow.
"""

import json
import logging
import re

from packages.ai.agents.state import RideShalaState

logger = logging.getLogger(__name__)

# Keywords for fallback intent detection (when LLM JSON parsing fails)
INTENT_KEYWORDS = {
    "compare": ["compare", "vs", "versus", "better", "difference", "which one"],
    "safety": ["safe", "safety", "abs", "helmet", "gear", "accident", "rain"],
    "tco": ["cost", "emi", "insurance", "rto", "expensive", "maintain", "tco", "own"],
    "ride_plan": ["plan", "ride", "route", "trip", "travel", "from", "to", "fuel stop"],
    "bike_search": ["best", "recommend", "suggest", "good", "buy", "under", "budget"],
}


def _fallback_classify(text: str) -> str:
    """Keyword-based intent detection when LLM fails."""
    text_lower = text.lower()
    for intent, keywords in INTENT_KEYWORDS.items():
        if any(kw in text_lower for kw in keywords):
            return intent
    return "general_chat"


def _extract_json(text: str) -> dict | None:
    """Extract JSON from LLM response, handling markdown code blocks."""
    # Try direct parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try extracting from markdown code block
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass

    # Try finding JSON object in text
    match = re.search(r"\{[^{}]*\}", text)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    return None


async def classify_intent_node(state: RideShalaState) -> dict:
    """Classify the user's intent using the best available LLM.

    Returns:
        Updated state with intent, bikes_mentioned, user_profile, and provider.
    """
    from packages.ai.llm.router import LLMRouter
    from packages.ai.prompts.system_base import INTENT_CLASSIFICATION_PROMPT

    last_message = state["messages"][-1]
    content = last_message.content if hasattr(last_message, "content") else str(last_message)

    router = LLMRouter()
    best_provider = await router.get_provider_for_task("classify")

    try:
        response = await router.generate(
            provider=best_provider,
            system=INTENT_CLASSIFICATION_PROMPT,
            messages=[{"role": "user", "content": content}],
            temperature=0.1,
            max_tokens=256,
        )

        result_text = response.choices[0].message.content
        result = _extract_json(result_text)

        if result:
            confidence = result.get("confidence", 0.7)
            intent = result.get("intent", "general_chat")

            if confidence <= 0.6:
                intent = "clarify"

            provider = await router.get_provider_for_task(intent)

            return {
                "intent": intent,
                "bikes_mentioned": result.get("bikes", []),
                "user_profile": result.get("profile"),
                "needs_clarification": confidence <= 0.6,
                "provider": provider,
            }
        else:
            # JSON parse failed — use keyword fallback
            logger.warning(f"LLM returned non-JSON, using keyword fallback: {result_text[:100]}")
            intent = _fallback_classify(content)
            return {
                "intent": intent,
                "bikes_mentioned": [],
                "user_profile": None,
                "needs_clarification": False,
                "provider": best_provider,
            }

    except Exception as e:
        logger.error(f"Intent classification failed: {e}")
        intent = _fallback_classify(content)
        return {
            "intent": intent,
            "bikes_mentioned": [],
            "needs_clarification": False,
            "provider": best_provider,
        }
