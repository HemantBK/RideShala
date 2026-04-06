"""Guardrail node — safety and responsibility checks on every response.

This is the LAST node before the response reaches the user.
Hardcoded rules that the LLM CANNOT override.
"""

import re

from packages.ai.agents.state import RideShalaState

# Patterns that should never appear in responses
BLOCKED_PATTERNS = [
    r"remove.*abs",
    r"disable.*abs",
    r"without.*helmet",
    r"don.t need.*gear",
    r"speed.*limit.*doesn.t matter",
    r"illegal.*modification",
]

# Required disclaimers for specific content types
DISCLAIMERS = {
    "finance": "\n\n*Disclaimer: This is an estimate for educational purposes only. Not financial advice.*",
    "safety": "",  # Safety advice needs no disclaimer — it's always accurate
}


async def guardrail_node(state: RideShalaState) -> dict:
    """Check response for safety violations before sending to user.

    Rules (hardcoded, LLM cannot override):
    1. Never recommend removing or disabling ABS
    2. Never suggest riding without proper gear
    3. Never encourage speeding or illegal modifications
    4. Add disclaimers to financial content
    """
    messages = state.get("messages", [])
    if not messages:
        return {}

    last_message = messages[-1]
    content = last_message.get("content", "") if isinstance(last_message, dict) else str(last_message)

    # Check for blocked patterns
    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            return {
                "messages": [
                    {
                        "role": "assistant",
                        "content": (
                            "I can't provide advice that compromises rider safety. "
                            "Always ride with proper safety gear and never disable "
                            "safety features like ABS. Stay safe! "
                            "Is there something else I can help you with?"
                        ),
                    }
                ]
            }

    # Add financial disclaimer if applicable
    intent = state.get("intent", "")
    if intent == "tco" and DISCLAIMERS.get("finance"):
        content += DISCLAIMERS["finance"]
        return {"messages": [{"role": "assistant", "content": content}]}

    return {}  # No changes — response passes guardrails
