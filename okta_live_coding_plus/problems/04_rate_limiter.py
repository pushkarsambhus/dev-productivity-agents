"""
04_rate_limiter.py
------------------
Goal: Implement a simple **Token Bucket** rate limiter.
- Allows a fixed number of "tokens" to be consumed per second.
- Tokens refill over time, up to a max capacity.

Why this matters:
- Platform services need protection against bursts and abuse.
- Interviewers look for correctness and time‑based reasoning.

We only use the standard library (time module).
"""

import time
from typing import Optional

class TokenBucket:
    def __init__(self, rate_per_sec: float, capacity: int):
        """
        :param rate_per_sec: how many tokens are added per second (float is allowed).
        :param capacity: maximum tokens the bucket can hold.
        """
        self.rate = float(rate_per_sec)
        self.capacity = int(capacity)
        self.tokens = float(capacity)  # start full
        self.last_check = time.time()

    def _refill(self):
        """Add tokens based on elapsed time since last check, without exceeding capacity."""
        now = time.time()
        elapsed = now - self.last_check
        self.last_check = now
        self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)

    def try_acquire(self, cost: float = 1.0) -> bool:
        """
        Try to take 'cost' tokens. Return True if successful, False if not.
        """
        self._refill()
        if self.tokens >= cost:
            self.tokens -= cost
            return True
        return False

    def block_until_acquire(self, cost: float = 1.0, timeout: Optional[float] = None) -> bool:
        """
        Block the caller until tokens are available or until 'timeout' seconds pass.
        Returns True if a token was acquired, False if timed out.
        """
        start = time.time()
        while True:
            if self.try_acquire(cost):
                return True
            if timeout is not None and (time.time() - start) >= timeout:
                return False
            # Sleep a bit to avoid busy waiting; sleeping less than 1/rate is reasonable.
            time.sleep(min(0.01, 1.0 / (self.rate + 1e-6)))


if __name__ == "__main__":
    # Simple demo: allow 5 requests per second with capacity 5.
    bucket = TokenBucket(rate_per_sec=5, capacity=5)
    acquired = 0
    start = time.time()
    while time.time() - start < 1.5:  # run for ~1.5 seconds
        if bucket.try_acquire():
            acquired += 1
        else:
            time.sleep(0.01)
    print("Acquired tokens in ~1.5s:", acquired)
