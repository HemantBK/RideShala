"""LLM provider router with fallback chain and circuit breakers.

DEFAULT: 100% free. vLLM (self-hosted Mistral 7B) handles ALL tasks.
OPTIONAL: If ANTHROPIC_API_KEY or GROQ_API_KEY are set, those providers
become available as quality upgrades, but they are NEVER required.

The system works fully with just vLLM — no paid API keys needed.
"""

import logging
import os

import pybreaker

logger = logging.getLogger(__name__)


class AllProvidersUnavailableError(Exception):
    """Raised when all LLM providers are down."""


class LLMRouter:
    """Route LLM requests to providers with fallback.

    Default behavior (FREE):
        vLLM handles everything — comparison, safety, TCO, chat.

    With optional paid keys:
        Claude can be enabled for complex tasks (comparison, safety, TCO).
        Groq can be enabled as a fast fallback.

    Fallback chain (always):
        vLLM (primary, free) -> Groq (if key set) -> Claude (if key set)
    """

    # Circuit breaker per provider
    BREAKERS = {
        "vllm": pybreaker.CircuitBreaker(fail_max=5, reset_timeout=60, name="vllm"),
        "claude": pybreaker.CircuitBreaker(fail_max=3, reset_timeout=60, name="claude"),
        "groq": pybreaker.CircuitBreaker(fail_max=5, reset_timeout=60, name="groq"),
    }

    def __init__(self):
        self.providers = {}

        # vLLM is the ONLY required provider — everything else is optional
        if os.getenv("VLLM_BASE_URL"):
            from packages.ai.llm.providers.vllm_provider import VLLMProvider
            self.providers["vllm"] = VLLMProvider()

        # Optional paid providers (only loaded if API key is set)
        anthropic_key = os.getenv("ANTHROPIC_API_KEY", "").strip()
        if anthropic_key and not anthropic_key.startswith("sk-ant-changeme"):
            from packages.ai.llm.providers.claude_provider import ClaudeProvider
            self.providers["claude"] = ClaudeProvider()
            logger.info("claude_provider_enabled (optional paid enhancement)")

        groq_key = os.getenv("GROQ_API_KEY", "").strip()
        if groq_key and not groq_key.startswith("gsk_changeme"):
            from packages.ai.llm.providers.groq_provider import GroqProvider
            self.providers["groq"] = GroqProvider()
            logger.info("groq_provider_enabled (optional free-tier fallback)")

        if not self.providers:
            raise RuntimeError(
                "No LLM providers configured. Set VLLM_BASE_URL in .env to point "
                "to your self-hosted vLLM server. No paid API keys are required."
            )

        logger.info(f"llm_router_ready providers={list(self.providers.keys())}")

    async def generate(
        self,
        provider: str = "vllm",
        messages: list[dict] | None = None,
        system: str | None = None,
        tools: list[dict] | None = None,
        temperature: float = 0.3,
        max_tokens: int = 2048,
        stream: bool = False,
    ):
        """Generate a response using the best available provider.

        Always tries vLLM first (free). Only uses paid providers if
        explicitly requested AND the API key is configured.
        """
        # Build fallback chain — vLLM is ALWAYS first
        chain = self._get_fallback_chain(provider)

        for p in chain:
            if p not in self.providers:
                continue

            breaker = self.BREAKERS.get(p)
            try:
                if breaker:
                    result = await breaker.call_async(
                        self.providers[p].generate,
                        messages=messages,
                        system=system,
                        tools=tools,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        stream=stream,
                    )
                else:
                    result = await self.providers[p].generate(
                        messages=messages,
                        system=system,
                        tools=tools,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        stream=stream,
                    )
                return result

            except pybreaker.CircuitBreakerError:
                logger.warning(f"Circuit breaker open for {p}, trying next provider")
                continue
            except Exception as e:
                logger.error(f"Provider {p} failed: {e}")
                continue

        raise AllProvidersUnavailableError(
            "All LLM providers are unavailable. Ensure vLLM is running."
        )

    def _get_fallback_chain(self, preferred: str) -> list[str]:
        """Build fallback chain. vLLM is always first unless Claude is explicitly requested."""
        if preferred == "claude" and "claude" in self.providers:
            return ["claude", "vllm", "groq"]
        if preferred == "groq" and "groq" in self.providers:
            return ["groq", "vllm"]
        # Default: vLLM first (free), then optional providers
        return ["vllm", "groq", "claude"]

    async def stream(self, provider: str = "vllm", **kwargs):
        """Stream a response. Convenience wrapper."""
        return await self.generate(provider=provider, stream=True, **kwargs)

    async def get_provider_for_task(self, task_type: str) -> str:
        """Get the best available provider for a task type.

        DEFAULT: Always returns "vllm" (free).
        Only returns "claude" if the API key is configured AND the task
        is complex enough to justify the cost.
        """
        # vLLM handles everything by default — it's free
        return "vllm"

    def get_status(self) -> dict:
        """Return health status of all providers."""
        return {
            name: {
                "available": name in self.providers,
                "circuit_state": str(self.BREAKERS[name].current_state),
                "is_free": name == "vllm",
                "is_optional_paid": name in ("claude", "groq"),
            }
            for name in ["vllm", "claude", "groq"]
        }
