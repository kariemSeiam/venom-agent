"""Exponential backoff with jitter for SIPHON daemon retries."""

from __future__ import annotations

import random


class BackoffController:
    """Increase interval on failure (capped at max); reset to base on success."""

    def __init__(
        self,
        *,
        base_interval: float = 5.0,
        max_interval: float = 120.0,
        jitter_fraction: float = 0.2,
    ) -> None:
        self.base_interval = base_interval
        self.max_interval = max_interval
        self.jitter_fraction = jitter_fraction
        self._interval = base_interval

    def reset(self) -> None:
        self._interval = self.base_interval

    def sleep_seconds_after_failure(self) -> float:
        capped = min(self.max_interval, self._interval)
        lo = capped * (1.0 - self.jitter_fraction)
        hi = capped * (1.0 + self.jitter_fraction)
        delay = random.uniform(lo, hi)
        self._interval = min(self.max_interval, max(self.base_interval, self._interval * 2.0))
        return delay
