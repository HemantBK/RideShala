"""LLM usage tracker — logs token usage for monitoring.

DEFAULT: All providers are FREE (vLLM self-hosted).
If optional paid providers (Claude, Groq) are enabled, their usage
is tracked for transparency. No budget is enforced by default
because the default setup costs nothing.
"""

from datetime import datetime

# Cost per 1M tokens — vLLM and Groq free tier cost NOTHING
# Claude costs are only relevant if user OPTIONALLY enables it
PRICING = {
    "vllm": {"input": 0.0, "output": 0.0},     # FREE — self-hosted
    "groq": {"input": 0.0, "output": 0.0},      # FREE — free tier
    "claude": {"input": 3.00, "output": 15.00},  # OPTIONAL PAID — only if user adds API key
}


class CostTracker:
    """Track LLM usage for monitoring and transparency.

    Default behavior: everything is free, tracking is for analytics only.
    If Claude API is optionally enabled, tracks spend for transparency.
    """

    def __init__(self, db_pool=None):
        self.db_pool = db_pool
        self._memory_log: list[dict] = []

    async def log_usage(
        self,
        provider: str,
        model: str,
        input_tokens: int,
        output_tokens: int,
        feature: str = "chat",
    ) -> float:
        """Log a single LLM API call and return its cost (0.0 for free providers)."""
        pricing = PRICING.get(provider, {"input": 0.0, "output": 0.0})
        cost = (input_tokens * pricing["input"] + output_tokens * pricing["output"]) / 1_000_000

        record = {
            "provider": provider,
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "feature": feature,
            "cost_usd": cost,
            "timestamp": datetime.now(datetime.UTC).isoformat(),
        }

        if self.db_pool:
            await self.db_pool.execute(
                """INSERT INTO usage_logs
                   (provider, model, input_tokens, output_tokens, feature, cost_usd, timestamp)
                   VALUES ($1, $2, $3, $4, $5, $6, NOW())""",
                provider, model, input_tokens, output_tokens, feature, cost,
            )
        else:
            self._memory_log.append(record)

        return cost

    async def get_daily_summary(self) -> list[dict]:
        """Get today's usage summary for monitoring."""
        today = datetime.now(datetime.UTC).date()
        return [
            r for r in self._memory_log
            if datetime.fromisoformat(r["timestamp"]).date() == today
        ]
