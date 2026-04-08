"""Lightweight async circuit breaker — replaces pybreaker.

pybreaker uses Tornado's @gen.coroutine which is broken on Python 3.13+.
This is a native async implementation in 40 lines. Zero external dependencies.

States:
    CLOSED  → Normal operation. Failures are counted.
    OPEN    → After fail_max failures, all calls are rejected for reset_timeout seconds.
    HALF_OPEN → After timeout, one call is allowed through. If it succeeds → CLOSED. If fails → OPEN.
"""

import time
import logging

logger = logging.getLogger(__name__)


class CircuitBreakerOpen(Exception):
    """Raised when the circuit breaker is OPEN and rejecting calls."""
    pass


class AsyncCircuitBreaker:
    """Native async circuit breaker. No Tornado, no pybreaker."""

    def __init__(self, name: str, fail_max: int = 5, reset_timeout: int = 60):
        self.name = name
        self.fail_max = fail_max
        self.reset_timeout = reset_timeout
        self.fail_count = 0
        self.last_failure_time = 0.0
        self.state = "closed"  # closed, open, half_open

    async def call(self, func, *args, **kwargs):
        """Call the async function with circuit breaker protection."""
        now = time.time()

        # If OPEN, check if timeout has passed
        if self.state == "open":
            if now - self.last_failure_time >= self.reset_timeout:
                self.state = "half_open"
                logger.info(f"circuit_breaker_half_open name={self.name}")
            else:
                raise CircuitBreakerOpen(f"Circuit breaker '{self.name}' is OPEN")

        try:
            result = await func(*args, **kwargs)
            # Success — reset to closed
            if self.state == "half_open":
                logger.info(f"circuit_breaker_closed name={self.name}")
            self.fail_count = 0
            self.state = "closed"
            return result

        except Exception as e:
            self.fail_count += 1
            self.last_failure_time = now

            if self.fail_count >= self.fail_max:
                self.state = "open"
                logger.warning(
                    f"circuit_breaker_opened name={self.name} "
                    f"failures={self.fail_count} timeout={self.reset_timeout}s"
                )

            raise e

    @property
    def current_state(self) -> str:
        return self.state
