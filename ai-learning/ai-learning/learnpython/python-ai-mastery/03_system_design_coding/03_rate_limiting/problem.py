"""
PHASE 3 | SYSTEM DESIGN CODING | 03 RATE LIMITING
==================================================
Topic: Implement a token bucket rate limiter — a real system component.
This appears in: LLM API gateways, CI/CD pipeline throttling, microservices.

In your Workday background: you've dealt with large-scale platform governance.
Rate limiting is a core pattern you'll be asked to code at principal level.

Algorithm: Token Bucket
- Bucket holds up to `capacity` tokens
- Tokens refill at `refill_rate` tokens/second
- Each request consumes 1 token
- If bucket is empty → request is rejected
"""
import time


class RateLimiter:
    """
    Token bucket rate limiter.

    Args:
        capacity: max tokens the bucket can hold
        refill_rate: tokens added per second
    """

    def __init__(self, capacity: int, refill_rate: float):
        # TODO: store capacity, refill_rate
        # TODO: set initial tokens to capacity (bucket starts full)
        # TODO: record the last refill timestamp (use time.time())
        pass

    def _refill(self):
        """Add tokens based on elapsed time since last refill."""
        # TODO:
        # 1. Calculate elapsed = now - last_refill
        # 2. Calculate new_tokens = elapsed * refill_rate
        # 3. Add to current tokens, but don't exceed capacity
        # 4. Update last_refill to now
        pass

    def allow_request(self) -> bool:
        """
        Returns True if the request is allowed, False if rate limited.
        """
        # TODO:
        # 1. Call _refill() to top up tokens
        # 2. If tokens >= 1: consume one token, return True
        # 3. Else: return False
        pass

    def __repr__(self):
        return f"RateLimiter(tokens={self.tokens:.2f}/{self.capacity}, rate={self.refill_rate}/s)"


# ── Bonus: Per-user rate limiter ───────────────────────────────────────────────
class PerUserRateLimiter:
    """
    Maintains a separate RateLimiter per user_id.
    Used in LLM APIs to enforce per-user quotas.
    """

    def __init__(self, capacity: int, refill_rate: float):
        # TODO: store params, create a dict to hold per-user limiters
        pass

    def allow_request(self, user_id: str) -> bool:
        # TODO: get or create a RateLimiter for user_id, then call allow_request()
        pass


# ── Self-check ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Basic rate limiter (5 tokens, 2/sec) ===")
    limiter = RateLimiter(capacity=5, refill_rate=2.0)

    # Burst: use all 5 tokens immediately
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
