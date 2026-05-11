"""
tracking/usage_reporter.py — Human-readable reporting and budget alerting.

UsageReporter ties together CostTracker and LatencyTracker to produce
reports suitable for:
  - Sharing with finance / business stakeholders (cost breakdown)
  - Engineering post-mortems (latency percentiles, SLA status)
  - Automated CI checks (budget_alert can gate a deployment)
"""

import json
import os
from datetime import datetime

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import SLA_LATENCY_P50_MS, SLA_LATENCY_P95_MS, MIN_QUALITY_SCORE
from tracking.cost_tracker import CostTracker
from tracking.latency_tracker import LatencyTracker


class UsageReporter:
    """
    Aggregates cost and latency data into formatted reports.

    Args:
        cost_tracker: A CostTracker instance that has been recording calls.
        latency_tracker: A LatencyTracker instance that has been recording times.
    """

    def __init__(self, cost_tracker: CostTracker, latency_tracker: LatencyTracker) -> None:
        self.cost_tracker = cost_tracker
        self.latency_tracker = latency_tracker

    def _build_report(self) -> dict:
        """Assemble the full report dict from both trackers."""
        cost_summary = self.cost_tracker.summary()
        latency_summary = self.latency_tracker.summary()

        overall_latency = latency_summary.get("overall", {})
        p50 = overall_latency.get("p50_ms", 0.0)
        p95 = overall_latency.get("p95_ms", 0.0)

        return {
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "cost": cost_summary,
            "latency": latency_summary,
            "sla_status": {
                "p50_target_ms": SLA_LATENCY_P50_MS,
                "p95_target_ms": SLA_LATENCY_P95_MS,
                "p50_actual_ms": p50,
                "p95_actual_ms": p95,
                "p50_within_sla": p50 <= SLA_LATENCY_P50_MS,
                "p95_within_sla": p95 <= SLA_LATENCY_P95_MS,
            },
        }

    def print_report(self) -> None:
        """
        Print a formatted, human-readable report to the console.
        Includes cost breakdown, latency percentiles, and SLA compliance status.
        """
        report = self._build_report()
        cost = report["cost"]
        latency = report["latency"]
        sla = report["sla_status"]
        overall = latency.get("overall", {})

        sep = "=" * 60

        print(f"\n{sep}")
        print("  USAGE REPORT")
        print(f"  Generated: {report['generated_at']}")
        print(sep)

        # --- Cost section ---
        print("\n  COST SUMMARY")
        print(f"  {'Total calls:':<35} {cost['total_calls']}")
        print(f"  {'Total cost (USD):':<35} ${cost['total_cost_usd']:.6f}")
        print(f"  {'Avg cost per call (USD):':<35} ${cost['avg_cost_per_call_usd']:.6f}")
        tokens = cost.get("total_tokens", {})
        print(f"  {'Total input tokens:':<35} {tokens.get('input', 0):,}")
        print(f"  {'Total output tokens:':<35} {tokens.get('output', 0):,}")
        print(f"  {'Total tokens:':<35} {tokens.get('total', 0):,}")

        if cost.get("cost_by_model"):
            print("\n  Cost by model:")
            for model, usd in cost["cost_by_model"].items():
                print(f"    {model:<40} ${usd:.6f}")

        # --- Latency section ---
        print("\n  LATENCY SUMMARY")
        print(f"  {'Total records:':<35} {latency['total_records']}")
        print(f"  {'P50 (median):':<35} {overall.get('p50_ms', 0):.1f} ms")
        print(f"  {'P95:':<35} {overall.get('p95_ms', 0):.1f} ms")
        print(f"  {'P99:':<35} {overall.get('p99_ms', 0):.1f} ms")
        print(f"  {'Mean:':<35} {overall.get('mean_ms', 0):.1f} ms")
        breach_pct = overall.get("sla_breach_rate", 0) * 100
        print(f"  {'SLA breach rate:':<35} {breach_pct:.1f}%")

        # --- Per-operation breakdown ---
        per_op = latency.get("per_operation", {})
        if per_op:
            print("\n  Latency by operation:")
            header = f"  {'Operation':<30} {'Count':>6} {'P50':>8} {'P95':>8} {'Breach%':>9}"
            print(header)
            print("  " + "-" * 58)
            for op, stats in per_op.items():
                print(
                    f"  {op:<30} {stats['count']:>6} "
                    f"{stats['p50_ms']:>7.0f}ms {stats['p95_ms']:>7.0f}ms "
                    f"{stats['sla_breach_rate']*100:>8.1f}%"
                )

        # --- SLA status ---
        print("\n  SLA COMPLIANCE")
        p50_ok = "PASS" if sla["p50_within_sla"] else "FAIL"
        p95_ok = "PASS" if sla["p95_within_sla"] else "FAIL"
        print(
            f"  P50: {sla['p50_actual_ms']:.1f}ms "
            f"(target ≤{sla['p50_target_ms']}ms) → {p50_ok}"
        )
        print(
            f"  P95: {sla['p95_actual_ms']:.1f}ms "
            f"(target ≤{sla['p95_target_ms']}ms) → {p95_ok}"
        )

        print(f"\n{sep}\n")

    def save_json(self, path: str) -> None:
        """
        Save the full report as a JSON file.

        Args:
            path: File path to write. Parent directories must exist.
        """
        report = self._build_report()
        # Include all individual call records for full auditability
        report["cost"]["calls"] = [c.to_dict() for c in self.cost_tracker.calls]
        report["latency"]["records"] = [r.to_dict() for r in self.latency_tracker.records]

        with open(path, "w", encoding="utf-8") as fh:
            json.dump(report, fh, indent=2)

    def budget_alert(self, budget_usd: float) -> bool:
        """
        Check whether the total cost has exceeded a budget threshold.

        Args:
            budget_usd: Maximum allowed spend in USD.

        Returns:
            True if over budget (alert should fire), False if within budget.

        Usage in CI:
            if reporter.budget_alert(5.00):
                raise SystemExit("Experiment exceeded $5.00 budget — aborting.")
        """
        total = self.cost_tracker.total_cost()
        over = total > budget_usd
        if over:
            print(
                f"[BUDGET ALERT] Spent ${total:.4f} exceeds budget of "
                f"${budget_usd:.4f} (overage: ${total - budget_usd:.4f})"
            )
        return over
