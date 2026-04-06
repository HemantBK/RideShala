"""vLLM provider — 100% FREE self-hosted LLM via OpenAI-compatible API.

Default model: Mistral 7B Instruct v0.3 (Apache 2.0, zero restrictions).
Alternative: Llama 3.1 8B (Llama License, 700M MAU commercial limit).

Uses the standard OpenAI Python SDK since vLLM exposes a fully
OpenAI-compatible API. No paid API keys required — runs on your own GPU.
"""

import os

from openai import AsyncOpenAI


class VLLMProvider:
    """Self-hosted LLM provider using vLLM with OpenAI-compatible API."""

    def __init__(self):
        self.client = AsyncOpenAI(
            base_url=os.getenv("VLLM_BASE_URL", "http://localhost:8000/v1"),
            api_key=os.getenv("VLLM_API_KEY", "dummy"),
        )
        self.model_name = os.getenv("VLLM_MODEL", "mistralai/Mistral-7B-Instruct-v0.3")

    async def generate(
        self,
        messages: list[dict],
        system: str | None = None,
        tools: list[dict] | None = None,
        temperature: float = 0.3,
        max_tokens: int = 2048,
        stream: bool = False,
    ):
        """Generate a response using vLLM.

        Args:
            messages: Chat messages in OpenAI format.
            system: System prompt (prepended as system message).
            tools: Tool definitions (vLLM supports function calling).
            temperature: Sampling temperature.
            max_tokens: Maximum tokens to generate.
            stream: Whether to stream the response.

        Returns:
            OpenAI ChatCompletion response.
        """
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
