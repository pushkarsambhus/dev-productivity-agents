"""
tracking/latency_tracker.py — API call latency measurement and SLA compliance.

Latency tracking is essential for:
- Validating that your AI feature meets UX expectations (users abandon after ~3s)
- Detecting model degradation or infra issues over time
- Comparing models fairly (Haiku is fast; Sonnet trades speed for quality)
- SLA reporting to customers or internal stakeholders
"""

import time
import statistics
from contextlib import contextmanager
from dataclasses import dataclass, asdict
from typing import Optional

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import SLA_LATENCY_P95_MS


@dataclass
class LatencyRecord:
    """A single timing observation for one API call or operation."""
    operation: str       # e.g. "chat", "summarize", "model_a_call"
    latency_ms: float    # elapsed time in milliseconds
    timestamp: float     # Unix epoch when the call *ended*
    model: str = ""      # optional: which model was used
    exceeded_sla: bool = False  # True if latency > SLA_LATENCY_P95_MS

    def to_dict(self) -> dict:
        return asdict(self)


class LatencyTracker:
    """
    Collects latency records and computes percentile statistics.

    Percentiles explained for non-engineers:
        P50 (median): Half of requests finish in this time or less. Good for "typical" UX.
        P95: 95% of requests finish by this time. This is what SLAs are usually written against
             because it captures tail latency — the slowest requests real users hit.
        P99: The worst 1% of requests. Important for detecting severe outliers.

    Example:
        tracker = LatencyTracker()
        with tracker.measure("model_b_call", model="claude-sonnet-4-6"):
            response = client.messages.create(...)
        print(f"P95: {tracker.p95():.0f}ms")
    """

    def __init__(self) -> None:
        self.records: list[LatencyRecord] = []

    def record(self, operation: str, latency_ms: float, model: str = "") -> LatencyRecord:
        """
        Manually record a latency observation.

        Args:
            operation: A string label for this type of call (e.g. "judge_call").
            latency_ms: How long the call took in milliseconds.
            model: Optional model name for filtering later.

        Returns:
            The created LatencyRecord.
        """
        exceeded = latency_ms > SLA_LATENCY_P95_MS
        rec = LatencyRecord(
            operation=operation,
            latency_ms=latency_ms,
            timestamp=time.time(),
            model=model,
            exceeded_sla=exceeded,
        )
        self.records.append(rec)
        return rec

    @contextmanager
    def measure(self, operation: str, model: str = ""):
        """
        Context manager that automatically times a block of code and records
        the elapsed time.

        Usage:
            with tracker.measure("summarize", model="claude-haiku-4-5-20251001"):
                response = client.messages.create(...)
        """
        start = time.perf_counter()
        try:
            yield
        finally:
            elapsed_ms = (time.perf_counter() - start) * 1000.0
            self.record(operation, elapsed_ms, model=model)

    def _latencies(self, operation: Optional[str] = None) -> list[float]:
        """Return latency values, optionally filtered by operation name."""
        if operation is None:
            return [r.latency_ms for r in self.records]
        return [r.latency_ms for r in self.records if r.operation == operation]

    def _percentile(self, values: list[float], pct: float) -> float:
        """
        Compute a percentile using linear interpolation (same as numpy's default).

        Args:
            values: List of numeric values.
            pct: Percentile as a fraction, e.g. 0.95 for P95.

        Returns:
            The interpolated percentile value, or 0.0 if the list is empty.
        """
        if not values:
            return 0.0
        sorted_vals = sorted(values)
        n = len(sorted_vals)
        if n == 1:
            return sorted_vals[0]
        # Linear interpolation between floor and ceiling indices
        rank = pct * (n - 1)
        lower = int(rank)
        upper = lower + 1
        if upper >= n:
            return sorted_vals[-1]
        frac = rank - lower
        return sorted_vals[lower] + frac * (sorted_vals[upper] - sorted_vals[lower])

    def p50(self, operation: Optional[str] = None) -> float:
        """Median latency in milliseconds."""
        return self._percentile(self._latencies(operation), 0.50)

    def p95(self, operation: Optional[str] = None) -> float:
        """95th percentile latency in milliseconds."""
        return self._percentile(self._latencies(operation), 0.95)

    def p99(self, operation: Optional[str] = None) -> float:
        """99th percentile latency in milliseconds."""
        return self._percentile(self._latencies(operation), 0.99)

    def sla_breach_rate(self, operation: Optional[str] = None) -> float:
        """
        Return the fraction of calls that exceeded SLA_LATENCY_P95_MS.

        Returns:
            A float between 0.0 and 1.0, e.g. 0.03 means 3% of calls breached SLA.
            Returns 0.0 if no records exist.
        """
        latencies = self._latencies(operation)
        if not latencies:
            return 0.0
        breaches = sum(1 for v in latencies if v > SLA_LATENCY_P95_MS)
        return breaches / len(latencies)

    def summary(self) -> dict:
        """
        Full statistical summary of all recorded latencies.
        """
        all_latencies = self._latencies()
        operations = list({r.operation for r in self.records})

        per_operation: dict[str, dict] = {}
        for op in operations:
            vals = self._latencies(op)
            per_operation[op] = {
                "count": len(vals),
                "p50_ms": round(self._percentile(vals, 0.50), 2),
                "p95_ms": round(self._percentile(vals, 0.95), 2),
                "p99_ms": round(self._percentile(vals, 0.99), 2),
                "sla_breach_rate": round(
                    sum(1 for v in vals if v > SLA_LATENCY_P95_MS) / len(vals), 4
                ) if vals else 0.0,
            }

        return {
            "total_records": len(self.records),
            "overall": {
                "p50_ms": round(self.p50(), 2),
                "p95_ms": round(self.p95(), 2),
                "p99_ms": round(self.p99(), 2),
                "sla_breach_rate": round(self.sla_breach_rate(), 4),
                "mean_ms": round(statistics.mean(all_latencies), 2) if all_latencies else 0.0,
                "min_ms": round(min(all_latencies), 2) if all_latencies else 0.0,
                "max_ms": round(max(all_latencies), 2) if all_latencies else 0.0,
            },
            "per_operation": per_operation,
            "sla_threshold_ms": SLA_LATENCY_P95_MS,
        }
