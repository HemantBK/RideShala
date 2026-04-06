"""Groq provider — fast inference fallback (free tier: 30 req/min).

Uses Groq's OpenAI-compatible API for fast inference on larger models
(Llama 3.1 70B) as a fallback when vLLM is down.
"""

import os

from openai import AsyncOpenAI


class GroqProvider:
    """Groq API provider for fast inference fallback."""

    def __init__(self):
        self.client = AsyncOpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=os.getenv("GROQ_API_KEY"),
        )
        self.model_name = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")

    async def generate(
        self,
        messages: list[dict],
        system: str | None = None,
        tools: list[dict] | None = None,
        temperature: float = 0.3,
        max_tokens: int = 2048,
        stream: bool = False,
    ):
        """Generate a response using Groq API."""
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
