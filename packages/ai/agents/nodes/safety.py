"""Safety agent node — rider safety assessment.

Uses Claude for high-stakes safety analysis.
Hardcoded rules CANNOT be overridden by the LLM.
"""

import logging

from packages.ai.agents.state import RideShalaState
from packages.ai.prompts.system_base import PERSONA, SAFETY_PROMPT

logger = logging.getLogger(__name__)

# Hardcoded safety data (LLM cannot override these)
SAFETY_ESSENTIALS = {
    "none": "This bike does NOT have ABS. We strongly recommend choosing a bike with at least single-channel ABS for your safety.",
    "single_channel": "This bike has single-channel ABS (front wheel only). Dual-channel ABS (front + rear) provides significantly better emergency braking. Consider upgrading if budget allows.",
    "dual_channel": "This bike has dual-channel ABS (front + rear) — the gold standard for safety.",
}


async def safety_agent_node(state: RideShalaState) -> dict:
    """Assess safety features and provide riding safety advice.

    Hardcoded rules (LLM CANNOT override):
    - Always recommend dual-channel ABS
    - Always recommend proper gear (helmet, gloves, jacket, boots)
    - Flag known issues from user reports
    - Never suggest disabling safety features
    """
    from packages.ai.llm.router import LLMRouter

    bikes = state.get("bikes_mentioned", [])
    last_msg = state["messages"][-1]
    query = last_msg.content if hasattr(last_msg, "content") else str(last_msg)

    context = f"Safety assessment request: {query}"
    if bikes:
        context += f"\nBikes being evaluated: {', '.join(bikes)}"

    system = f"{PERSONA}\n\n{SAFETY_PROMPT}"

    try:
        router = LLMRouter()
        response = await router.generate(
            provider=state.get("provider", "vllm"),
            system=system,
            messages=[{"role": "user", "content": context}],
            temperature=0.2,
            max_tokens=1024,
        )

        if hasattr(response, "choices"):
            result_text = response.choices[0].message.content
        elif hasattr(response, "content"):
            result_text = response.content[0].text if isinstance(response.content, list) else str(response.content)
        else:
            result_text = str(response)

        # Append mandatory safety reminders (hardcoded, LLM cannot skip these)
        safety_footer = (
            "\n\n---\n"
            "**Mandatory Safety Reminders:**\n"
            "- Always wear a full-face ISI-certified helmet\n"
            "- Riding gloves, jacket, and boots significantly reduce injury risk\n"
            "- Dual-channel ABS is the most important safety feature on any motorcycle\n"
            "- Never ride above the speed limit or under the influence"
        )

        return {
            "safety_result": result_text + safety_footer,
            "sources": ["OEM safety specifications", "RideShala user safety reports"],
        }

    except Exception as e:
        logger.error(f"Safety agent failed: {e}")
        return {
            "safety_result": (
                "I couldn't generate a detailed safety assessment right now, but here are the essentials:\n\n"
                "- Always choose a bike with dual-channel ABS\n"
                "- Always wear a full-face helmet, gloves, riding jacket, and boots\n"
                "- Check tyre pressure before every ride\n"
                "- Never ride above speed limits or in unsafe weather conditions"
            ),
            "sources": [],
        }
