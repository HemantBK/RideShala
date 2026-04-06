"""Claude provider — Anthropic API for complex reasoning tasks.

Used for tasks that need nuanced reasoning: multi-bike comparisons,
safety assessments, and TCO analysis with detailed explanations.
"""

import os

import anthropic


class ClaudeProvider:
    """Anthropic Claude provider for premium reasoning tasks."""

    def __init__(self):
        self.client = anthropic.AsyncAnthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY"),
        )
        self.model_name = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-20250514")

    async def generate(
        self,
        messages: list[dict],
        system: str | None = None,
        tools: list[dict] | None = None,
        temperature: float = 0.3,
        max_tokens: int = 4096,
        stream: bool = False,
    ):
        """Generate a response using Claude.

        Args:
            messages: Chat messages (converted from OpenAI to Anthropic format).
            system: System prompt (passed via Anthropic's native system parameter).
            tools: Tool definitions for Claude's tool_use feature.
            temperature: Sampling temperature.
            max_tokens: Maximum tokens to generate.
            stream: Whether to stream the response.

        Returns:
            Anthropic Message response.
        """
        # Convert OpenAI-format messages to Anthropic format
        anthropic_messages = self._convert_messages(messages)

        kwargs = {
            "model": self.model_name,
            "max_tokens": max_tokens,
            "messages": anthropic_messages,
            "temperature": temperature,
        }

        if system:
            kwargs["system"] = system

        if tools:
            kwargs["tools"] = self._convert_tools(tools)

        if stream:
            return self.client.messages.stream(**kwargs)

        return await self.client.messages.create(**kwargs)

    def _convert_messages(self, messages: list[dict]) -> list[dict]:
        """Convert OpenAI-format messages to Anthropic format.

        Strips system messages (handled via the system parameter) and
        maps assistant/user roles.
        """
        converted = []
        for msg in messages:
            if msg["role"] == "system":
                continue  # System messages handled separately
            converted.append({"role": msg["role"], "content": msg["content"]})
        return converted

    def _convert_tools(self, tools: list[dict]) -> list[dict]:
        """Convert OpenAI-format tool definitions to Anthropic format."""
        return [
            {
                "name": tool["name"],
                "description": tool.get("description", ""),
                "input_schema": tool.get("input_schema", tool.get("parameters", {})),
            }
            for tool in tools
        ]
