"""
tests/test_cost_tracker.py — Unit tests for cost and latency tracking.

These tests do NOT require an Anthropic API key. They test the tracking
logic in isolation using mock objects.

Run with:
    pytest tests/test_cost_tracker.py -v
"""

import time
import sys
import os

# Make the project root importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from tracking.cost_tracker import CostTracker, CallCost, calculate_cost
from tracking.latency_tracker import LatencyTracker, LatencyRecord
from tracking.usage_reporter import UsageReporter
from config import TOKEN_PRICING, SLA_LATENCY_P95_MS


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

class FakeUsage:
    """Mock of anthropic.types.Usage — only has input_tokens and output_tokens."""
    def __init__(self, input_tokens: int, output_tokens: int):
        self.input_tokens = input_tokens
        self.output_tokens = output_tokens


# ─────────────────────────────────────────────────────────────────────────────
# TestCalculateCost
# ─────────────────────────────────────────────────────────────────────────────

class TestCalculateCost:
    """Tests for the standalone calculate_cost() function."""

    def test_haiku_pricing_exact(self):
        """
        Verify Haiku pricing math:
          input=$0.80/M, output=$4.00/M
          1,000,000 in + 1,000,000 out = $0.80 + $4.00 = $4.80
        """
        cost = calculate_cost("claude-haiku-4-5-20251001", 1_000_000, 1_000_000)
        assert abs(cost - 4.80) < 1e-9, f"Expected $4.80, got ${cost}"

    def test_haiku_pricing_small(self):
        """Test with small token counts (realistic per-call values)."""
        # 500 input tokens at $0.80/M = $0.00040
        # 200 output tokens at $4.00/M = $0.00080
        # Total = $0.00120
        cost = calculate_cost("claude-haiku-4-5-20251001", 500, 200)
        expected = (500 / 1_000_000) * 0.80 + (200 / 1_000_000) * 4.00
        assert abs(cost - expected) < 1e-10

    def test_sonnet_pricing_exact(self):
        """
        Verify Sonnet pricing math:
          input=$3.00/M, output=$15.00/M
          1,000,000 in + 1,000,000 out = $3.00 + $15.00 = $18.00
        """
        cost = calculate_cost("claude-sonnet-4-6", 1_000_000, 1_000_000)
        assert abs(cost - 18.00) < 1e-9, f"Expected $18.00, got ${cost}"

    def test_sonnet_vs_haiku_ratio(self):
        """
        Sonnet should cost more than Haiku for the same token counts.
        This verifies the models are priced correctly relative to each other.
        """
        tokens_in, tokens_out = 1000, 500
        haiku_cost = calculate_cost("claude-haiku-4-5-20251001", tokens_in, tokens_out)
        sonnet_cost = calculate_cost("claude-sonnet-4-6", tokens_in, tokens_out)
        assert sonnet_cost > haiku_cost, "Sonnet should cost more than Haiku"

    def test_zero_tokens(self):
        """Zero tokens should produce zero cost."""
        cost = calculate_cost("claude-haiku-4-5-20251001", 0, 0)
        assert cost == 0.0

    def test_zero_input_tokens(self):
        """Zero input tokens: cost should come only from output tokens."""
        cost = calculate_cost("claude-haiku-4-5-20251001", 0, 1_000_000)
        expected = (1_000_000 / 1_000_000) * 4.00
        assert abs(cost - expected) < 1e-9

    def test_zero_output_tokens(self):
        """Zero output tokens: cost should come only from input tokens."""
        cost = calculate_cost("claude-haiku-4-5-20251001", 1_000_000, 0)
        expected = (1_000_000 / 1_000_000) * 0.80
        assert abs(cost - expected) < 1e-9

    def test_unknown_model_returns_zero(self):
        """Unknown model names should return 0.0, not raise an exception."""
        cost = calculate_cost("nonexistent-model-xyz", 1000, 500)
        assert cost == 0.0, "Unknown model should return 0.0 cost"

    def test_all_configured_models_present(self):
        """Every model in TOKEN_PRICING should produce a positive cost."""
        for model in TOKEN_PRICING:
            cost = calculate_cost(model, 1000, 500)
            assert cost > 0.0, f"Model {model} should produce positive cost"


# ─────────────────────────────────────────────────────────────────────────────
# TestCostTracker
# ─────────────────────────────────────────────────────────────────────────────

class TestCostTracker:
    """Tests for the CostTracker class."""

    def setup_method(self):
        """Create a fresh tracker before each test."""
        self.tracker = CostTracker()

    def test_initial_state_empty(self):
        """New tracker should have no calls and zero cost."""
        assert len(self.tracker.calls) == 0
        assert self.tracker.total_cost() == 0.0

    def test_record_returns_call_cost(self):
        """record() should return a CallCost dataclass."""
        usage = FakeUsage(input_tokens=1000, output_tokens=500)
        result = self.tracker.record("claude-haiku-4-5-20251001", usage)
        assert isinstance(result, CallCost)
        assert result.model == "claude-haiku-4-5-20251001"
        assert result.input_tokens == 1000
        assert result.output_tokens == 500

    def test_record_appends_to_calls(self):
        """Each call to record() should append to self.calls."""
        usage = FakeUsage(500, 200)
        self.tracker.record("claude-haiku-4-5-20251001", usage)
        assert len(self.tracker.calls) == 1
        self.tracker.record("claude-haiku-4-5-20251001", usage)
        assert len(self.tracker.calls) == 2

    def test_record_computes_cost_correctly(self):
        """record() should compute costs using TOKEN_PRICING."""
        # 1M input + 1M output for Haiku = $4.80
        usage = FakeUsage(1_000_000, 1_000_000)
        call = self.tracker.record("claude-haiku-4-5-20251001", usage)
        assert abs(call.input_cost_usd - 0.80) < 1e-9
        assert abs(call.output_cost_usd - 4.00) < 1e-9
        assert abs(call.total_cost_usd - 4.80) < 1e-9

    def test_total_cost_sums_all_calls(self):
        """total_cost() should sum costs across all recorded calls."""
        haiku_usage = FakeUsage(1_000_000, 1_000_000)
        self.tracker.record("claude-haiku-4-5-20251001", haiku_usage)
        self.tracker.record("claude-haiku-4-5-20251001", haiku_usage)
        # Two Haiku calls at $4.80 each = $9.60
        assert abs(self.tracker.total_cost() - 9.60) < 1e-6

    def test_total_cost_empty(self):
        """total_cost() returns 0.0 when no calls have been recorded."""
        assert self.tracker.total_cost() == 0.0

    def test_total_tokens_sums_correctly(self):
        """total_tokens() should aggregate input, output, and total."""
        self.tracker.record("claude-haiku-4-5-20251001", FakeUsage(100, 50))
        self.tracker.record("claude-haiku-4-5-20251001", FakeUsage(200, 100))
        tokens = self.tracker.total_tokens()
        assert tokens["input"] == 300
        assert tokens["output"] == 150
        assert tokens["total"] == 450

    def test_cost_by_model_groups_correctly(self):
        """cost_by_model() should group costs by model name."""
        haiku_usage = FakeUsage(1_000_000, 0)  # $0.80 each
        sonnet_usage = FakeUsage(1_000_000, 0)  # $3.00 each

        self.tracker.record("claude-haiku-4-5-20251001", haiku_usage)
        self.tracker.record("claude-haiku-4-5-20251001", haiku_usage)
        self.tracker.record("claude-sonnet-4-6", sonnet_usage)

        by_model = self.tracker.cost_by_model()
        assert "claude-haiku-4-5-20251001" in by_model
        assert "claude-sonnet-4-6" in by_model
        assert abs(by_model["claude-haiku-4-5-20251001"] - 1.60) < 1e-6  # 2 * $0.80
        assert abs(by_model["claude-sonnet-4-6"] - 3.00) < 1e-6

    def test_cost_by_model_empty(self):
        """cost_by_model() should return empty dict when no calls recorded."""
        assert self.tracker.cost_by_model() == {}

    def test_summary_structure(self):
        """summary() should return a dict with the expected keys."""
        self.tracker.record("claude-haiku-4-5-20251001", FakeUsage(100, 50))
        s = self.tracker.summary()
        assert "total_calls" in s
        assert "total_cost_usd" in s
        assert "total_tokens" in s
        assert "cost_by_model" in s
        assert s["total_calls"] == 1

    def test_summary_with_multiple_calls(self):
        """summary() should correctly reflect multiple calls."""
        for _ in range(5):
            self.tracker.record("claude-haiku-4-5-20251001", FakeUsage(100, 50))
        s = self.tracker.summary()
        assert s["total_calls"] == 5
        assert s["total_cost_usd"] > 0

    def test_reset_clears_all_calls(self):
        """reset() should empty self.calls."""
        self.tracker.record("claude-haiku-4-5-20251001", FakeUsage(100, 50))
        assert len(self.tracker.calls) == 1
        self.tracker.reset()
        assert len(self.tracker.calls) == 0
        assert self.tracker.total_cost() == 0.0

    def test_reset_then_record(self):
        """After reset(), new calls should be tracked normally."""
        self.tracker.record("claude-haiku-4-5-20251001", FakeUsage(100, 50))
        self.tracker.reset()
        self.tracker.record("claude-sonnet-4-6", FakeUsage(200, 100))
        assert len(self.tracker.calls) == 1
        assert self.tracker.calls[0].model == "claude-sonnet-4-6"

    def test_timestamp_is_recent(self):
        """CallCost timestamp should be close to the current time."""
        before = time.time()
        call = self.tracker.record("claude-haiku-4-5-20251001", FakeUsage(100, 50))
        after = time.time()
        assert before <= call.timestamp <= after


# ─────────────────────────────────────────────────────────────────────────────
# TestLatencyTracker
# ─────────────────────────────────────────────────────────────────────────────

class TestLatencyTracker:
    """Tests for the LatencyTracker class."""

    def setup_method(self):
        self.tracker = LatencyTracker()

    def test_record_returns_latency_record(self):
        """record() should return a LatencyRecord."""
        rec = self.tracker.record("api_call", 1500.0, model="claude-haiku-4-5-20251001")
        assert isinstance(rec, LatencyRecord)
        assert rec.operation == "api_call"
        assert rec.latency_ms == 1500.0
        assert rec.model == "claude-haiku-4-5-20251001"

    def test_record_marks_sla_breach(self):
        """Latency above SLA_LATENCY_P95_MS should be marked exceeded_sla=True."""
        high_latency = SLA_LATENCY_P95_MS + 1
        rec = self.tracker.record("slow_call", float(high_latency))
        assert rec.exceeded_sla is True

    def test_record_no_sla_breach(self):
        """Latency at or below threshold should have exceeded_sla=False."""
        rec = self.tracker.record("fast_call", float(SLA_LATENCY_P95_MS))
        assert rec.exceeded_sla is False

    def test_p50_with_known_values(self):
        """P50 should return the median of the recorded latencies."""
        # 5 known values: [100, 200, 300, 400, 500] → median = 300
        for v in [100.0, 200.0, 300.0, 400.0, 500.0]:
            self.tracker.record("op", v)
        assert abs(self.tracker.p50() - 300.0) < 1e-6

    def test_p95_with_known_values(self):
        """P95 should return the 95th percentile."""
        # 20 values: 1, 2, ..., 20 (ascending). P95 = index 18.05 by linear interp
        for v in range(1, 21):
            self.tracker.record("op", float(v))
        p95 = self.tracker.p95()
        # P95 of 1..20: rank = 0.95 * 19 = 18.05 → 19 + 0.05*(20-19) = 19.05
        assert abs(p95 - 19.05) < 0.1

    def test_p99_with_known_values(self):
        """P99 should return the 99th percentile."""
        for v in range(1, 101):
            self.tracker.record("op", float(v))
        p99 = self.tracker.p99()
        # P99 of 1..100: rank = 0.99 * 99 = 98.01 → 99 + 0.01*(100-99) = 99.01
        assert abs(p99 - 99.01) < 0.1

    def test_percentiles_single_value(self):
        """With one value, all percentiles should return that value."""
        self.tracker.record("op", 1234.5)
        assert self.tracker.p50() == 1234.5
        assert self.tracker.p95() == 1234.5
        assert self.tracker.p99() == 1234.5

    def test_percentiles_empty_returns_zero(self):
        """Percentiles on empty tracker should return 0.0."""
        assert self.tracker.p50() == 0.0
        assert self.tracker.p95() == 0.0
        assert self.tracker.p99() == 0.0

    def test_percentile_filter_by_operation(self):
        """p50(operation=) should filter to only that operation's records."""
        for v in [100.0, 200.0, 300.0]:
            self.tracker.record("fast_op", v)
        for v in [1000.0, 2000.0, 3000.0]:
            self.tracker.record("slow_op", v)

        # P50 for fast_op should be ~200 (median of 100,200,300)
        fast_p50 = self.tracker.p50("fast_op")
        assert abs(fast_p50 - 200.0) < 1e-6

        # P50 for slow_op should be ~2000 (median of 1000,2000,3000)
        slow_p50 = self.tracker.p50("slow_op")
        assert abs(slow_p50 - 2000.0) < 1e-6

    def test_measure_context_manager(self):
        """measure() should record elapsed time as a LatencyRecord."""
        with self.tracker.measure("test_block"):
            time.sleep(0.01)  # 10ms

        assert len(self.tracker.records) == 1
        rec = self.tracker.records[0]
        assert rec.operation == "test_block"
        # Should be at least 10ms but not more than 500ms (generous for CI)
        assert 5.0 < rec.latency_ms < 500.0

    def test_measure_records_model(self):
        """measure() should store the model name when provided."""
        with self.tracker.measure("call", model="claude-haiku-4-5-20251001"):
            pass  # no-op

        assert self.tracker.records[0].model == "claude-haiku-4-5-20251001"

    def test_sla_breach_rate_no_breaches(self):
        """Breach rate should be 0.0 when all latencies are within SLA."""
        for _ in range(10):
            self.tracker.record("op", 1000.0)  # well under SLA
        assert self.tracker.sla_breach_rate() == 0.0

    def test_sla_breach_rate_all_breach(self):
        """Breach rate should be 1.0 when all latencies exceed SLA."""
        for _ in range(5):
            self.tracker.record("op", float(SLA_LATENCY_P95_MS + 100))
        assert self.tracker.sla_breach_rate() == 1.0

    def test_sla_breach_rate_partial(self):
        """Breach rate should be the fraction exceeding the threshold."""
        # 2 of 10 exceed SLA → 20%
        for _ in range(8):
            self.tracker.record("op", 1000.0)  # within SLA
        for _ in range(2):
            self.tracker.record("op", float(SLA_LATENCY_P95_MS + 100))
        assert abs(self.tracker.sla_breach_rate() - 0.2) < 1e-9

    def test_sla_breach_rate_empty(self):
        """Empty tracker should return 0.0 breach rate."""
        assert self.tracker.sla_breach_rate() == 0.0

    def test_summary_structure(self):
        """summary() should return a dict with expected top-level keys."""
        self.tracker.record("op", 1000.0)
        s = self.tracker.summary()
        assert "total_records" in s
        assert "overall" in s
        assert "per_operation" in s
        assert "sla_threshold_ms" in s

    def test_summary_per_operation(self):
        """summary() per_operation should group by operation name."""
        for v in [100.0, 200.0, 300.0]:
            self.tracker.record("search", v)
        for v in [500.0, 600.0]:
            self.tracker.record("embed", v)
        s = self.tracker.summary()
        assert "search" in s["per_operation"]
        assert "embed" in s["per_operation"]
        assert s["per_operation"]["search"]["count"] == 3
        assert s["per_operation"]["embed"]["count"] == 2


# ─────────────────────────────────────────────────────────────────────────────
# TestUsageReporter
# ─────────────────────────────────────────────────────────────────────────────

class TestUsageReporter:
    """Tests for UsageReporter.budget_alert() and save_json()."""

    def setup_method(self):
        self.cost_tracker = CostTracker()
        self.latency_tracker = LatencyTracker()
        self.reporter = UsageReporter(self.cost_tracker, self.latency_tracker)

    def test_budget_alert_under_budget(self):
        """Should return False when spending is below the budget."""
        # Record a small cost
        self.cost_tracker.record("claude-haiku-4-5-20251001", FakeUsage(100, 50))
        actual_cost = self.cost_tracker.total_cost()
        # Budget is 10x the actual cost
        result = self.reporter.budget_alert(actual_cost * 10)
        assert result is False

    def test_budget_alert_over_budget(self):
        """Should return True when spending exceeds the budget."""
        # Record enough calls to exceed $0.01 budget
        for _ in range(100):
            self.cost_tracker.record("claude-haiku-4-5-20251001", FakeUsage(10_000, 5_000))
        actual_cost = self.cost_tracker.total_cost()
        # Budget is 1% of what we spent → over budget
        result = self.reporter.budget_alert(actual_cost * 0.01)
        assert result is True

    def test_budget_alert_exactly_at_budget(self):
        """At exactly budget, should NOT trigger alert (strictly greater than)."""
        self.cost_tracker.record("claude-haiku-4-5-20251001", FakeUsage(1_000_000, 0))
        exact_cost = self.cost_tracker.total_cost()
        # Exactly at budget → not over
        result = self.reporter.budget_alert(exact_cost)
        assert result is False

    def test_budget_alert_zero_cost(self):
        """With no API calls, budget alert should always be False."""
        result = self.reporter.budget_alert(0.01)
        assert result is False

    def test_save_json_creates_file(self, tmp_path):
        """save_json() should create a valid JSON file at the specified path."""
        import json

        self.cost_tracker.record("claude-haiku-4-5-20251001", FakeUsage(100, 50))
        self.latency_tracker.record("op", 500.0)

        output_path = str(tmp_path / "report.json")
        self.reporter.save_json(output_path)

        assert os.path.exists(output_path)
        with open(output_path) as f:
            data = json.load(f)

        assert "cost" in data
        assert "latency" in data
        assert "sla_status" in data

    def test_print_report_runs_without_error(self, capsys):
        """print_report() should not raise exceptions and produce output."""
        self.cost_tracker.record("claude-haiku-4-5-20251001", FakeUsage(500, 200))
        self.latency_tracker.record("test_op", 1200.0)

        self.reporter.print_report()

        captured = capsys.readouterr()
        assert "USAGE REPORT" in captured.out
        assert "COST SUMMARY" in captured.out
        assert "LATENCY SUMMARY" in captured.out
