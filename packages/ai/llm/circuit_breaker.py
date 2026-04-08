"""Lightweight async circuit breaker — replaces pybreaker.

pybreaker uses Tornado's @gen.coroutine which is broken on Python 3.13+.
This is a native async implementation. Zero external dependencies.

States:
    CLOSED  -> Normal. Failures counted.
    OPEN    -> After fail_max failures, all calls rejected for reset_timeout seconds.
    HALF_OPEN -> After timeout, one call allowed. Success -> CLOSED. Fail -> OPEN.
"""

import logging
import time

logger = logging.getLogger(__name__)


class CircuitBreakerOpenError(Exception):
    """Raised when the circuit breaker is OPEN and rejecting calls."""


class AsyncCircuitBreaker:
    """Native async circuit breaker. No Tornado, no pybreaker."""

    def __init__(self, name: str, fail_max: int = 5, reset_timeout: int = 60):
        self.name = name
        self.fail_max = fail_max
        self.reset_timeout = reset_timeout
        self.fail_count = 0
        self.last_failure_time = 0.0
        self.state = "closed"

    async def call(self, func, *args, **kwargs):
        """Call the async function with circuit breaker protection."""
        now = time.time()

        if self.state == "open":
            if now - self.last_failure_time >= self.reset_timeout:
                self.state = "half_open"
                logger.info(f"circuit_breaker_half_open name={self.name}")
            else:
                raise CircuitBreakerOpenError(f"Circuit breaker '{self.name}' is OPEN")

        try:
            result = await func(*args, **kwargs)
            if self.state == "half_open":
                logger.info(f"circuit_breaker_closed name={self.name}")
            self.fail_count = 0
            self.state = "closed"
            return result

        except Exception:
            self.fail_count += 1
            self.last_failure_time = now

            if self.fail_count >= self.fail_max:
                self.state = "open"
                logger.warning(
                    f"circuit_breaker_opened name={self.name} "
                    f"failures={self.fail_count} timeout={self.reset_timeout}s"
                )

            raise

    @property
    def current_state(self) -> str:
        return self.state
