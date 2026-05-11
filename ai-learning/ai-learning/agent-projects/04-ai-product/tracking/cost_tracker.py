"""
tracking/cost_tracker.py — Per-call API cost tracking.

WHY COST TRACKING MATTERS
==========================
1. Budget forecasting: If you know each call to Haiku costs ~$0.002 and you
   expect 100,000 calls/day, you can project $200/day before you ship.

2. Per-feature cost attribution: "The summarization feature costs 3× more than
   the Q&A feature because responses are longer." You can't optimize what you
   don't measure.

3. Alerting: Set a daily budget threshold. If you're at 80% of budget by noon,
   trigger an alert before you overspend.

4. Model selection: Tracking actual costs (not just list prices) reveals whether
   Sonnet's higher quality justifies its 3.75× price premium for your workload.

5. Cost per user / cost per transaction: Essential for pricing and unit economics.
   "Our AI feature costs $0.04 per conversation on average."

Usage example:
    tracker = CostTracker()
    response = client.messages.create(...)
    call = tracker.record(model, response.usage)
    print(f"This call cost ${call.total_cost_usd:.6f}")
    print(tracker.summary())
"""

import time
from dataclasses import dataclass, field, asdict
from typing import Any

# Use sys.path trick to allow imports from parent directory when run standalone
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import TOKEN_PRICING


@dataclass
class CallCost:
    """Cost record for a single API call."""
    model: str
    input_tokens: int
    output_tokens: int
    input_cost_usd: float
    output_cost_usd: float
    total_cost_usd: float
    timestamp: float  # Unix epoch seconds

    def to_dict(self) -> dict:
        return asdict(self)


class CostTracker:
    """
    Accumulates cost records across multiple API calls.

    Typical usage pattern:
        tracker = CostTracker()
        # ... make API calls, record each one ...
        print(tracker.summary())
    """

    def __init__(self) -> None:
        self.calls: list[CallCost] = []

    def record(self, model: str, usage: Any) -> CallCost:
        """
        Record the cost of one API call.

        Args:
            model: The model name (must be in TOKEN_PRICING).
            usage: The Anthropic SDK Usage object (has .input_tokens and .output_tokens).

        Returns:
            A CallCost dataclass with all cost fields populated.

        Note on pricing math:
            TOKEN_PRICING stores cost per *million* tokens.
            cost = (tokens / 1_000_000) * price_per_million
        """
        input_tokens: int = getattr(usage, "input_tokens", 0)
        output_tokens: int = getattr(usage, "output_tokens", 0)

        pricing = TOKEN_PRICING.get(model, {"input": 0.0, "output": 0.0})

        input_cost = (input_tokens / 1_000_000) * pricing["input"]
        output_cost = (output_tokens / 1_000_000) * pricing["output"]
        total_cost = input_cost + output_cost

        call = CallCost(
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            input_cost_usd=input_cost,
            output_cost_usd=output_cost,
            total_cost_usd=total_cost,
            timestamp=time.time(),
        )
        self.calls.append(call)
        return call

    def total_cost(self) -> float:
        """Return the total USD cost across all recorded calls."""
        return sum(c.total_cost_usd for c in self.calls)

    def total_tokens(self) -> dict[str, int]:
        """
        Return aggregated token counts.

        Returns:
            {"input": N, "output": N, "total": N}
        """
        input_total = sum(c.input_tokens for c in self.calls)
        output_total = sum(c.output_tokens for c in self.calls)
        return {
            "input": input_total,
            "output": output_total,
            "total": input_total + output_total,
        }

    def cost_by_model(self) -> dict[str, float]:
        """
        Return total cost grouped by model name.

        Example:
            {"claude-haiku-4-5-20251001": 0.0012, "claude-sonnet-4-6": 0.0045}
        """
        costs: dict[str, float] = {}
        for call in self.calls:
            costs[call.model] = costs.get(call.model, 0.0) + call.total_cost_usd
        return costs

    def summary(self) -> dict:
        """
        Return a full summary dict suitable for logging or JSON serialization.
        """
        tokens = self.total_tokens()
        return {
            "total_calls": len(self.calls),
            "total_cost_usd": self.total_cost(),
            "total_tokens": tokens,
            "cost_by_model": self.cost_by_model(),
            "avg_cost_per_call_usd": (
                self.total_cost() / len(self.calls) if self.calls else 0.0
            ),
            "avg_tokens_per_call": (
                tokens["total"] / len(self.calls) if self.calls else 0
            ),
        }

    def reset(self) -> None:
        """Clear all recorded calls. Useful between experiment runs."""
        self.calls = []


def calculate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    """
    Standalone function: compute the USD cost for a single call without
    creating a tracker instance. Useful for quick estimates.

    Args:
        model: Model name (must exist in TOKEN_PRICING, else returns 0.0).
        input_tokens: Number of prompt/input tokens.
        output_tokens: Number of completion/output tokens.

    Returns:
        Total cost in USD as a float.

    Example:
        # How much does a 1000-token prompt + 500-token response cost on Haiku?
        cost = calculate_cost("claude-haiku-4-5-20251001", 1000, 500)
        # => (1000/1e6 * 0.80) + (500/1e6 * 4.00) = $0.0008 + $0.002 = $0.0028 — wait
        # Actually: 0.00080 + 0.00200 = $0.00280 — but at scale:
        # 1M such calls = $2,800. That's why cost tracking matters.
    """
    pricing = TOKEN_PRICING.get(model, {"input": 0.0, "output": 0.0})
    input_cost = (input_tokens / 1_000_000) * pricing["input"]
    output_cost = (output_tokens / 1_000_000) * pricing["output"]
    return input_cost + output_cost
