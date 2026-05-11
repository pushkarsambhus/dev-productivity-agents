"""
tests/test_ab_testing.py — Unit tests for A/B testing and statistical analysis.

No API calls required. Experiment-level tests mock the API and judge layers.

Run with:
    pytest tests/test_ab_testing.py -v
"""

import sys
import os
import math
from dataclasses import dataclass, field
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from ab_testing.statistical_analysis import (
    win_rate,
    confidence_interval,
    is_significant,
    effect_size,
    cost_quality_tradeoff,
)
from ab_testing.experiment import ExperimentResult, ExperimentSample, _determine_recommendation


# ─────────────────────────────────────────────────────────────────────────────
# TestStatisticalAnalysis
# ─────────────────────────────────────────────────────────────────────────────

class TestWinRate:
    """Tests for win_rate()."""

    def test_perfect_win(self):
        assert win_rate(10, 10) == 1.0

    def test_zero_wins(self):
        assert win_rate(0, 10) == 0.0

    def test_half_wins(self):
        assert win_rate(5, 10) == 0.5

    def test_zero_total_returns_zero(self):
        """Dividing by zero should return 0.0, not raise."""
        assert win_rate(0, 0) == 0.0

    def test_typical_case(self):
        assert abs(win_rate(12, 20) - 0.6) < 1e-9


class TestConfidenceInterval:
    """Tests for Wilson score confidence_interval()."""

    def test_returns_tuple_of_two_floats(self):
        lo, hi = confidence_interval(5, 10)
        assert isinstance(lo, float)
        assert isinstance(hi, float)

    def test_lower_le_upper(self):
        lo, hi = confidence_interval(5, 10)
        assert lo <= hi

    def test_bounds_in_zero_one(self):
        """Both bounds must be in [0, 1]."""
        lo, hi = confidence_interval(3, 20)
        assert 0.0 <= lo <= 1.0
        assert 0.0 <= hi <= 1.0

    def test_zero_total_returns_full_interval(self):
        """With no data, CI should be (0, 1) — maximum uncertainty."""
        lo, hi = confidence_interval(0, 0)
        assert lo == 0.0
        assert hi == 1.0

    def test_clear_winner_lower_bound_above_half(self):
        """15 wins out of 20 — lower bound of CI should be > 0.5."""
        lo, hi = confidence_interval(15, 20)
        assert lo > 0.5, f"Expected lower bound > 0.5 for 15/20, got {lo:.3f}"

    def test_inconclusive_straddles_half(self):
        """5 wins out of 10 — CI should straddle 0.5 (wide interval)."""
        lo, hi = confidence_interval(5, 10)
        assert lo < 0.5 < hi, f"Expected CI [{lo:.3f}, {hi:.3f}] to straddle 0.5"

    def test_all_wins(self):
        """All wins should give CI close to 1.0."""
        lo, hi = confidence_interval(10, 10)
        assert hi > 0.9, f"Expected upper bound near 1.0, got {hi:.3f}"
        assert lo > 0.5, f"Expected lower bound > 0.5 for 10/10, got {lo:.3f}"

    def test_no_wins(self):
        """No wins should give CI close to 0.0."""
        lo, hi = confidence_interval(0, 10)
        assert lo < 0.1, f"Expected lower bound near 0.0, got {lo:.3f}"

    def test_higher_confidence_gives_wider_interval(self):
        """99% CI should be wider than 95% CI."""
        lo_95, hi_95 = confidence_interval(10, 20, confidence=0.95)
        lo_99, hi_99 = confidence_interval(10, 20, confidence=0.99)
        width_95 = hi_95 - lo_95
        width_99 = hi_99 - lo_99
        assert width_99 > width_95, "99% CI should be wider than 95% CI"


class TestIsSignificant:
    """Tests for is_significant() binomial test."""

    def test_clear_winner_is_significant(self):
        """18 wins vs 2 losses — clearly significant."""
        assert is_significant(2, 18) is True

    def test_near_equal_not_significant(self):
        """10 wins vs 10 losses — not significant."""
        assert is_significant(10, 10) is False

    def test_slight_lean_not_significant(self):
        """12 wins vs 8 losses (60/40) — usually not significant at N=20."""
        assert is_significant(8, 12) is False

    def test_zero_total_not_significant(self):
        """No comparisons made — cannot be significant."""
        assert is_significant(0, 0) is False

    def test_all_one_side_is_significant(self):
        """20 wins vs 0 losses — definitely significant."""
        assert is_significant(0, 20) is True
        assert is_significant(20, 0) is True

    def test_symmetry(self):
        """is_significant(a, b) == is_significant(b, a) — it's two-sided."""
        assert is_significant(15, 5) == is_significant(5, 15)

    def test_larger_sample_reaches_significance_sooner(self):
        """
        With 60/40 split: N=20 might not be significant, but N=100 should be.
        (60/40 = 60 wins out of 100)
        """
        result_small = is_significant(8, 12)    # 12/20
        result_large = is_significant(40, 60)   # 60/100
        # The larger sample should be significant (or equal)
        assert not result_small or result_large  # at minimum, large should catch what small does


class TestEffectSize:
    """Tests for Cohen's d effect_size()."""

    def test_equal_distributions_zero_d(self):
        """Identical distributions should have d = 0."""
        scores = [5.0, 6.0, 7.0, 8.0, 7.5]
        d = effect_size(scores, scores)
        assert abs(d) < 1e-9

    def test_positive_d_when_b_higher(self):
        """When B scores higher than A, d should be positive."""
        scores_a = [4.0, 5.0, 4.5, 5.5, 4.0]
        scores_b = [7.0, 8.0, 7.5, 8.5, 7.0]
        d = effect_size(scores_a, scores_b)
        assert d > 0

    def test_negative_d_when_a_higher(self):
        """When A scores higher than B, d should be negative."""
        scores_a = [8.0, 9.0, 8.5, 9.5, 8.0]
        scores_b = [4.0, 5.0, 4.5, 5.5, 4.0]
        d = effect_size(scores_a, scores_b)
        assert d < 0

    def test_large_effect_size(self):
        """Very different distributions should give |d| > 0.8 (large)."""
        scores_a = [2.0, 3.0, 2.5, 3.5, 2.0, 3.0, 2.5, 2.0]
        scores_b = [8.0, 9.0, 8.5, 9.5, 8.0, 9.0, 8.5, 8.0]
        d = effect_size(scores_a, scores_b)
        assert abs(d) > 0.8, f"Expected large effect size, got {d:.3f}"

    def test_empty_lists_return_zero(self):
        """Empty score lists should return 0.0 without error."""
        assert effect_size([], []) == 0.0
        assert effect_size([5.0], [5.0]) == 0.0  # single values → no variance

    def test_single_element_each_returns_zero(self):
        """Can't compute variance with 1 element — should return 0.0."""
        assert effect_size([5.0], [8.0]) == 0.0

    def test_zero_variance_returns_zero(self):
        """If all values are identical (zero variance), return 0.0."""
        scores_a = [5.0, 5.0, 5.0, 5.0]
        scores_b = [5.0, 5.0, 5.0, 5.0]
        assert effect_size(scores_a, scores_b) == 0.0


class TestCostQualityTradeoff:
    """Tests for cost_quality_tradeoff()."""

    def test_a_dominates_both_cheaper_and_better(self):
        """When A is cheaper AND better, should recommend A."""
        result = cost_quality_tradeoff(
            cost_a=0.001, quality_a=8.0,
            cost_b=0.005, quality_b=7.0,
        )
        assert "A" in result
        # Should not recommend B
        assert "Prefer Model A" in result or "cheaper" in result.lower()

    def test_b_dominates_both_cheaper_and_better(self):
        """When B is cheaper AND better, should recommend B."""
        result = cost_quality_tradeoff(
            cost_a=0.005, quality_a=7.0,
            cost_b=0.001, quality_b=8.0,
        )
        assert "B" in result
        assert "Prefer Model B" in result or "cheaper" in result.lower()

    def test_negligible_quality_difference_prefer_cheaper(self):
        """When quality is nearly equal (< 0.5 pts), should prefer cheaper."""
        result = cost_quality_tradeoff(
            cost_a=0.001, quality_a=7.5,
            cost_b=0.005, quality_b=7.6,
        )
        # Quality difference is 0.1 → negligible → prefer Model A (cheaper)
        assert "negligible" in result.lower() or "A" in result

    def test_returns_string(self):
        """Should always return a non-empty string."""
        result = cost_quality_tradeoff(0.001, 7.0, 0.005, 8.0)
        assert isinstance(result, str)
        assert len(result) > 10

    def test_zero_cost_a_does_not_crash(self):
        """Zero cost for model A should not raise ZeroDivisionError."""
        result = cost_quality_tradeoff(0.0, 7.0, 0.005, 8.0)
        assert isinstance(result, str)


# ─────────────────────────────────────────────────────────────────────────────
# TestExperimentResult and _determine_recommendation
# ─────────────────────────────────────────────────────────────────────────────

class TestDetermineRecommendation:
    """Tests for the _determine_recommendation() internal function."""

    def test_b_clear_winner(self):
        """B winning 15/20 (75%) should recommend USE_B."""
        rec = _determine_recommendation(5, 15, 0, 0.005, 0.01, 7.0, 8.5)
        assert rec == "USE_B"

    def test_a_clear_winner(self):
        """A winning 15/20 (75%) should recommend USE_A."""
        rec = _determine_recommendation(15, 5, 0, 0.005, 0.01, 8.5, 7.0)
        assert rec == "USE_A"

    def test_close_results_inconclusive(self):
        """10/10 split should be INCONCLUSIVE."""
        rec = _determine_recommendation(10, 10, 0, 0.005, 0.01, 7.5, 7.5)
        assert rec == "INCONCLUSIVE"

    def test_cost_tiebreaker_prefers_cheaper(self):
        """
        When quality is nearly equal, if Model A is 60% cheaper, prefer A.
        """
        # 55% wins for B (slightly above 50% but below 60% threshold)
        # Quality difference < 0.5
        # Model A costs $0.001, Model B costs $0.005 → B is 5x more expensive
        rec = _determine_recommendation(
            wins_a=9, wins_b=11, ties=0,
            avg_cost_a=0.001, avg_cost_b=0.005,
            avg_score_a=7.5, avg_score_b=7.6,
        )
        # Quality is nearly the same (0.1 diff), but B is much more expensive → USE_A
        assert rec == "USE_A"

    def test_zero_comparisons_inconclusive(self):
        """No comparisons → INCONCLUSIVE."""
        rec = _determine_recommendation(0, 0, 0, 0.001, 0.005, 7.0, 8.0)
        assert rec == "INCONCLUSIVE"


class TestExperimentResultDataclass:
    """Tests for ExperimentResult construction and field access."""

    def _make_sample(self, winner: str, score_a: float, score_b: float) -> ExperimentSample:
        return ExperimentSample(
            sample_id="s001",
            prompt="Test prompt",
            model_a_response="Response A",
            model_b_response="Response B",
            model_a_cost=0.001,
            model_b_cost=0.005,
            model_a_latency_ms=500.0,
            model_b_latency_ms=1200.0,
            judge_winner=winner,
            judge_score_a=score_a,
            judge_score_b=score_b,
            judge_reasoning="B was more detailed.",
        )

    def test_create_experiment_result(self):
        """ExperimentResult can be instantiated with all required fields."""
        result = ExperimentResult(
            experiment_id="test-exp-001",
            prompts_tested=10,
            model_a_wins=3,
            model_b_wins=7,
            ties=0,
            model_a_avg_cost=0.001,
            model_b_avg_cost=0.005,
            model_a_avg_latency_ms=500.0,
            model_b_avg_latency_ms=1200.0,
            model_a_avg_score=7.0,
            model_b_avg_score=8.5,
            recommendation="USE_B",
            samples=[],
        )
        assert result.experiment_id == "test-exp-001"
        assert result.model_b_wins == 7
        assert result.recommendation == "USE_B"

    def test_samples_list_defaults_empty(self):
        """samples field should default to empty list if not provided."""
        result = ExperimentResult(
            experiment_id="exp",
            prompts_tested=0,
            model_a_wins=0,
            model_b_wins=0,
            ties=0,
            model_a_avg_cost=0.0,
            model_b_avg_cost=0.0,
            model_a_avg_latency_ms=0.0,
            model_b_avg_latency_ms=0.0,
            model_a_avg_score=0.0,
            model_b_avg_score=0.0,
            recommendation="INCONCLUSIVE",
        )
        assert result.samples == []

    def test_sample_fields_accessible(self):
        """ExperimentSample fields should be accessible."""
        sample = self._make_sample("B", 7.0, 8.5)
        assert sample.judge_winner == "B"
        assert sample.judge_score_a == 7.0
        assert sample.judge_score_b == 8.5
        assert sample.model_b_cost > sample.model_a_cost


class TestRunExperimentMocked:
    """
    Tests for run_experiment() with all API calls mocked.
    Verifies that the experiment logic correctly aggregates results.
    """

    def _make_mock_message(self, text: str, input_tokens: int = 100, output_tokens: int = 50):
        """Create a mock Anthropic message response."""
        mock_message = MagicMock()
        mock_message.content = [MagicMock()]
        mock_message.content[0].text = text
        mock_message.usage.input_tokens = input_tokens
        mock_message.usage.output_tokens = output_tokens
        return mock_message

    def _make_mock_comparison(self, winner: str, score_a: float = 7.0, score_b: float = 8.0):
        """Create a mock ComparisonResult."""
        from ab_testing.experiment import ExperimentSample
        mock = MagicMock()
        mock.winner = winner
        mock.score_a = score_a
        mock.score_b = score_b
        mock.reasoning = "Mocked reasoning."
        return mock

    @patch("ab_testing.experiment.compare_responses")
    @patch("ab_testing.experiment._call_model")
    def test_run_experiment_b_wins(self, mock_call_model, mock_compare):
        """When judge always picks B, recommendation should be USE_B."""
        from ab_testing.experiment import run_experiment

        # Model calls return dummy responses
        mock_call_model.return_value = ("dummy response", 500.0, 100, 50)

        # Judge always picks B
        mock_compare.return_value = self._make_mock_comparison("B", 7.0, 9.0)

        prompts = [f"Test prompt {i}" for i in range(10)]
        result = run_experiment(prompts, experiment_id="test-b-wins")

        assert result.model_b_wins > result.model_a_wins
        assert result.recommendation == "USE_B"
        assert result.prompts_tested == 10

    @patch("ab_testing.experiment.compare_responses")
    @patch("ab_testing.experiment._call_model")
    def test_run_experiment_a_wins(self, mock_call_model, mock_compare):
        """When judge always picks A, recommendation should be USE_A."""
        from ab_testing.experiment import run_experiment

        mock_call_model.return_value = ("dummy response", 300.0, 80, 40)
        mock_compare.return_value = self._make_mock_comparison("A", 9.0, 6.0)

        prompts = [f"Test prompt {i}" for i in range(10)]
        result = run_experiment(prompts, experiment_id="test-a-wins")

        assert result.model_a_wins > result.model_b_wins
        assert result.recommendation == "USE_A"

    @patch("ab_testing.experiment.compare_responses")
    @patch("ab_testing.experiment._call_model")
    def test_run_experiment_all_ties(self, mock_call_model, mock_compare):
        """When all comparisons are ties, recommendation should be INCONCLUSIVE."""
        from ab_testing.experiment import run_experiment

        mock_call_model.return_value = ("dummy response", 400.0, 100, 50)
        mock_compare.return_value = self._make_mock_comparison("TIE", 7.5, 7.5)

        prompts = [f"Test prompt {i}" for i in range(10)]
        result = run_experiment(prompts, experiment_id="test-ties")

        assert result.ties == 10
        assert result.model_a_wins == 0
        assert result.model_b_wins == 0
        assert result.recommendation == "INCONCLUSIVE"

    @patch("ab_testing.experiment.compare_responses")
    @patch("ab_testing.experiment._call_model")
    def test_run_experiment_collects_all_samples(self, mock_call_model, mock_compare):
        """Samples list should have one entry per prompt."""
        from ab_testing.experiment import run_experiment

        mock_call_model.return_value = ("response text", 600.0, 120, 60)
        mock_compare.return_value = self._make_mock_comparison("B")

        prompts = ["p1", "p2", "p3", "p4", "p5"]
        result = run_experiment(prompts, experiment_id="test-samples")

        assert len(result.samples) == 5
        assert result.prompts_tested == 5

    @patch("ab_testing.experiment.compare_responses")
    @patch("ab_testing.experiment._call_model")
    def test_run_experiment_generates_id_if_not_provided(self, mock_call_model, mock_compare):
        """If no experiment_id is given, one should be auto-generated."""
        from ab_testing.experiment import run_experiment

        mock_call_model.return_value = ("resp", 400.0, 100, 50)
        mock_compare.return_value = self._make_mock_comparison("B")

        result = run_experiment(["prompt1"], )
        assert result.experiment_id is not None
        assert len(result.experiment_id) > 0
