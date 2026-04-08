"""Google Gemini provider — free tier available.

Uses Google's OpenAI-compatible endpoint for Gemini models.
Free tier: Gemini 2.5 Flash (5-20 RPM, 250K TPM).

Get free key: https://aistudio.google.com/apikey
"""

import os

from openai import AsyncOpenAI


class GeminiProvider:
    """Google Gemini via OpenAI-compatible API."""

    def __init__(self):
        self.client = AsyncOpenAI(
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
            api_key=os.getenv("GEMINI_API_KEY"),
        )
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

    async def generate(
        self,
        messages: list[dict],
        system: str | None = None,
        tools: list[dict] | None = None,
        temperature: float = 0.3,
        max_tokens: int = 2048,
        stream: bool = False,
    ):
        """Generate a response using Gemini."""
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
