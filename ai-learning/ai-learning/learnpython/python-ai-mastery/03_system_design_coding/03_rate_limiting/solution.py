"""
SOLUTION: Phase 3 | System Design Coding | 03 Rate Limiting
"""
import time


class RateLimiter:
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = float(capacity)   # start full
        self.last_refill = time.time()

    def _refill(self):
        now = time.time()
        elapsed = now - self.last_refill
        new_tokens = elapsed * self.refill_rate
        self.tokens = min(self.capacity, self.tokens + new_tokens)
        self.last_refill = now
        # min() enforces the bucket ceiling — can't exceed capacity

    def allow_request(self) -> bool:
        self._refill()
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False
        # Notice: return bool directly — no if/else needed (Pylint R1703)

    def __repr__(self):
        return f"RateLimiter(tokens={self.tokens:.2f}/{self.capacity}, rate={self.refill_rate}/s)"


class PerUserRateLimiter:
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self._limiters: dict[str, RateLimiter] = {}

    def allow_request(self, user_id: str) -> bool:
        if user_id not in self._limiters:
            self._limiters[user_id] = RateLimiter(self.capacity, self.refill_rate)
        return self._limiters[user_id].allow_request()
        # dict.setdefault() is an alternative:
        # self._limiters.setdefault(user_id, RateLimiter(...)).allow_request()


# ── Interview talking points ───────────────────────────────────────────────────
"""
Q: Why token bucket over fixed window?
A: Fixed window has burst problem — user can use double quota at window boundary.
   Token bucket smooths this out.

Q: Is this thread-safe?
A: No — in production you'd use threading.Lock() around allow_request(),
   or implement this in Redis with atomic INCR/EXPIRE for distributed systems.

Q: How would you scale this across multiple servers?
A: Move state to Redis. Use a Lua script for atomic check-and-decrement.
   This is how LLM API gateways (OpenAI, Anthropic) implement per-user limits.
"""

if __name__ == "__main__":
    print("=== Basic rate limiter (5 tokens, 2/sec) ===")
    limiter = RateLimiter(capacity=5, refill_rate=2.0)
    for i in range(7):
        result = limiter.allow_request()
        print(f"  Request {i+1}: {'✓ allowed' if result else '✗ denied'}")

    print("\nWaiting 1 second to refill...")
    time.sleep(1)
    print(f"  Request after wait: {'✓ allowed' if limiter.allow_request() else '✗ denied'}")

    print("\n=== Per-user rate limiter ===")
    per_user = PerUserRateLimiter(capacity=3, refill_rate=1.0)
    for req in ["alice", "alice", "alice", "alice", "bob", "bob"]:
        result = per_user.allow_request(req)
        print(f"  {req}: {'✓' if result else '✗'}")
