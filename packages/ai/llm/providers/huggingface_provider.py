"""HuggingFace Inference provider — 100% free, no rate limit worries.

Uses HuggingFace's OpenAI-compatible router endpoint.
Free tier: ~100 requests/hour with HF token.
Models: Llama 3.1 8B, Mistral 7B, Qwen 2.5 72B — all open source.

Get your free token: https://huggingface.co/settings/tokens
"""

import os

from openai import AsyncOpenAI


class HuggingFaceProvider:
    """HuggingFace free inference via OpenAI-compatible API."""

    def __init__(self):
        self.client = AsyncOpenAI(
            base_url="https://router.huggingface.co/v1",
            api_key=os.getenv("HF_TOKEN"),
        )
        self.model_name = os.getenv(
            "HF_MODEL", "meta-llama/Llama-3.1-8B-Instruct"
        )

    async def generate(
        self,
        messages: list[dict],
        system: str | None = None,
        tools: list[dict] | None = None,
        temperature: float = 0.3,
        max_tokens: int = 2048,
        stream: bool = False,
    ):
        """Generate a response using HuggingFace free inference."""
        full_messages = []
        if system:
            full_messages.append({"role": "system", "content": system})
        full_messages.extend(messages)

        kwargs = {
            "model": self.model_name,
            "messages": full_messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream,
        }

        if tools:
            kwargs["tools"] = [{"type": "function", "function": t} for t in tools]

        return await self.client.chat.completions.create(**kwargs)
