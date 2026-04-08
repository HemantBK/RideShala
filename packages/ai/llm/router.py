"""LLM provider router with fallback chain and circuit breakers.

DEFAULT: 100% free. vLLM (self-hosted Mistral 7B) handles ALL tasks.
OPTIONAL: If ANTHROPIC_API_KEY or GROQ_API_KEY are set, those providers
become available as quality upgrades, but they are NEVER required.

The system works fully with just vLLM — no paid API keys needed.
"""

import logging
import os

from packages.ai.llm.circuit_breaker import AsyncCircuitBreaker, CircuitBreakerOpen

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

    # Circuit breaker per provider (native async, no Tornado dependency)
    BREAKERS = {
        "vllm": AsyncCircuitBreaker(name="vllm", fail_max=5, reset_timeout=60),
        "claude": AsyncCircuitBreaker(name="claude", fail_max=3, reset_timeout=60),
        "groq": AsyncCircuitBreaker(name="groq", fail_max=5, reset_timeout=60),
        "huggingface": AsyncCircuitBreaker(name="huggingface", fail_max=5, reset_timeout=60),
        "gemini": AsyncCircuitBreaker(name="gemini", fail_max=5, reset_timeout=60),
    }

    def __init__(self):
        self.providers = {}

        # vLLM — free, self-hosted (needs GPU)
        if os.getenv("VLLM_BASE_URL"):
            from packages.ai.llm.providers.vllm_provider import VLLMProvider
            self.providers["vllm"] = VLLMProvider()
            logger.info("vllm_provider_enabled (free, self-hosted)")

        # Groq — free tier, 30 req/min, no GPU needed
        groq_key = os.getenv("GROQ_API_KEY", "").strip()
        if groq_key and not groq_key.startswith("gsk_changeme") and not groq_key.startswith("gsk_your"):
            from packages.ai.llm.providers.groq_provider import GroqProvider
            self.providers["groq"] = GroqProvider()
            logger.info("groq_provider_enabled (free tier)")

        # HuggingFace — free, ~100 req/hour
        hf_token = os.getenv("HF_TOKEN", "").strip()
        if hf_token and not hf_token.startswith("hf_changeme"):
            from packages.ai.llm.providers.huggingface_provider import HuggingFaceProvider
            self.providers["huggingface"] = HuggingFaceProvider()
            logger.info("huggingface_provider_enabled (free)")

        # Gemini — free tier (Flash models)
        gemini_key = os.getenv("GEMINI_API_KEY", "").strip()
        if gemini_key and not gemini_key.startswith("changeme"):
            from packages.ai.llm.providers.gemini_provider import GeminiProvider
            self.providers["gemini"] = GeminiProvider()
            logger.info("gemini_provider_enabled (free tier)")

        # Claude — optional paid enhancement
        anthropic_key = os.getenv("ANTHROPIC_API_KEY", "").strip()
        if anthropic_key and not anthropic_key.startswith("sk-ant-changeme"):
            from packages.ai.llm.providers.claude_provider import ClaudeProvider
            self.providers["claude"] = ClaudeProvider()
            logger.info("claude_provider_enabled (optional paid)")

        if not self.providers:
            raise RuntimeError(
                "No LLM providers configured. Set one of these in .env:\n"
                "  - GROQ_API_KEY (free, no GPU — groq.com)\n"
                "  - HF_TOKEN (free — huggingface.co/settings/tokens)\n"
                "  - VLLM_BASE_URL (free, needs GPU)\n"
                "  - ANTHROPIC_API_KEY (optional paid — claude.ai)"
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
                    result = await breaker.call(
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

            except CircuitBreakerOpen:
                logger.warning(f"Circuit breaker open for {p}, trying next provider")
                continue
            except Exception as e:
                logger.error(f"Provider {p} failed: {e}")
                continue

        raise AllProvidersUnavailableError(
            "All LLM providers are unavailable. Ensure vLLM is running."
        )

    def _get_fallback_chain(self, preferred: str) -> list[str]:
        """Build fallback chain with all available providers."""
        if preferred == "claude" and "claude" in self.providers:
            return ["claude", "groq", "huggingface", "vllm"]
        if preferred in self.providers:
            chain = [preferred]
        else:
            chain = []
        # Add all other providers as fallbacks
        for p in ["vllm", "groq", "gemini", "huggingface", "claude"]:
            if p not in chain:
                chain.append(p)
        return chain

    async def stream(self, provider: str = "vllm", **kwargs):
        """Stream a response. Convenience wrapper."""
        return await self.generate(provider=provider, stream=True, **kwargs)

    async def get_provider_for_task(self, task_type: str) -> str:
        """Get the best available provider for a task type.

        Returns the first available provider in priority order.
        """
        priority = ["vllm", "groq", "claude"]
        for p in priority:
            if p in self.providers:
                return p
        return next(iter(self.providers))

    def get_status(self) -> dict:
        """Return health status of all providers."""
        return {
            name: {
                "available": name in self.providers,
                "circuit_state": str(self.BREAKERS[name].current_state),
                "is_free": name == "vllm",
                "is_optional_paid": name in ("claude", "groq"),
            }
            for name in ["vllm", "groq", "gemini", "huggingface", "claude"]
        }
