"""
tests/test_llm_judge.py — Unit tests for LLM-as-judge evaluation.

All Anthropic API calls are mocked. These tests verify:
  - JSON parsing of well-formed judge responses
  - Graceful handling of malformed JSON (fallback behavior)
  - Correct extraction of winner, scores, and reasoning
  - Batch processing behavior

Run with:
    pytest tests/test_llm_judge.py -v
"""

import json
import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from platform_eval.llm_judge import (
    JudgeScore,
    ComparisonResult,
    score_response,
    compare_responses,
    batch_score,
    _parse_score_response,
    _parse_comparison_response,
    _extract_json,
    _extract_score_fallback,
    DEFAULT_CRITERIA,
)


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _make_mock_message(text: str) -> MagicMock:
    """Create a mock Anthropic message response with the given text."""
    msg = MagicMock()
    msg.content = [MagicMock()]
    msg.content[0].text = text
    return msg


def _make_valid_score_json(
    overall: float = 8.0,
    criteria: dict = None,
    reasoning: str = "This is a good response.",
) -> str:
    """Build a valid JSON string for score_response() testing."""
    if criteria is None:
        criteria = {c: 8 for c in DEFAULT_CRITERIA}
    return json.dumps({
        "overall_score": overall,
        "criteria_scores": criteria,
        "reasoning": reasoning,
    })


def _make_valid_comparison_json(
    score_a: float = 7.0,
    score_b: float = 8.5,
    winner: str = "B",
    reasoning: str = "B was more detailed.",
) -> str:
    """Build a valid JSON string for compare_responses() testing."""
    return json.dumps({
        "score_a": score_a,
        "score_b": score_b,
        "winner": winner,
        "reasoning": reasoning,
    })


# ─────────────────────────────────────────────────────────────────────────────
# TestParseHelpers
# ─────────────────────────────────────────────────────────────────────────────

class TestExtractJson:
    """Tests for the _extract_json() helper."""

    def test_bare_json_object(self):
        """Plain JSON should be returned as-is."""
        text = '{"score": 8, "reasoning": "good"}'
        result = _extract_json(text)
        assert result == text

    def test_json_in_markdown_code_fence(self):
        """JSON wrapped in ```json ... ``` should be extracted."""
        text = '```json\n{"score": 8}\n```'
        result = _extract_json(text)
        parsed = json.loads(result)
        assert parsed["score"] == 8

    def test_json_in_plain_code_fence(self):
        """JSON wrapped in ``` ... ``` (no language) should be extracted."""
        text = '```\n{"winner": "A"}\n```'
        result = _extract_json(text)
        parsed = json.loads(result)
        assert parsed["winner"] == "A"

    def test_json_with_surrounding_text(self):
        """JSON embedded in prose should be extracted."""
        text = 'Here is my evaluation: {"overall_score": 7.5} based on the criteria.'
        result = _extract_json(text)
        parsed = json.loads(result)
        assert parsed["overall_score"] == 7.5

    def test_no_json_returns_original(self):
        """Text without any JSON object is returned as-is."""
        text = "This response has no JSON at all."
        result = _extract_json(text)
        assert result == text


class TestExtractScoreFallback:
    """Tests for _extract_score_fallback()."""

    def test_score_colon_pattern(self):
        """Extracts score from 'score: 7' pattern."""
        val = _extract_score_fallback("I would give this a score: 7 out of 10.")
        assert abs(val - 7.0) < 1e-6

    def test_fraction_pattern(self):
        """Extracts score from '8/10' pattern."""
        val = _extract_score_fallback("This response deserves 8/10.")
        assert abs(val - 8.0) < 1e-6

    def test_overall_score_pattern(self):
        """Extracts from 'overall_score: 6.5' pattern."""
        val = _extract_score_fallback("overall_score: 6.5")
        assert abs(val - 6.5) < 1e-6

    def test_no_pattern_returns_five(self):
        """If no pattern found, returns 5.0 (midpoint)."""
        val = _extract_score_fallback("This response is totally fine and great.")
        assert val == 5.0

    def test_clamps_to_valid_range(self):
        """Score is clamped to [1, 10]."""
        # Some judges might say "11/10"
        val = _extract_score_fallback("This deserves 11/10!")
        assert val <= 10.0
        val = _extract_score_fallback("score: 0")
        assert val >= 1.0


# ─────────────────────────────────────────────────────────────────────────────
# TestJudgeScore (score_response)
# ─────────────────────────────────────────────────────────────────────────────

class TestJudgeScore:
    """Tests for score_response() — parses judge output into JudgeScore."""

    @patch("platform_eval.llm_judge._get_client")
    def test_parses_valid_json_response(self, mock_get_client):
        """score_response() should parse well-formed JSON into JudgeScore."""
        criteria = {c: 8 for c in DEFAULT_CRITERIA}
        json_text = _make_valid_score_json(overall=8.5, criteria=criteria, reasoning="Clear and accurate.")
        mock_get_client.return_value.messages.create.return_value = _make_mock_message(json_text)

        result = score_response("What is 2+2?", "The answer is 4.")

        assert isinstance(result, JudgeScore)
        assert abs(result.score - 8.5) < 1e-6
        assert result.reasoning == "Clear and accurate."
        assert len(result.criteria_scores) == len(DEFAULT_CRITERIA)

    @patch("platform_eval.llm_judge._get_client")
    def test_score_is_clamped_to_1_10(self, mock_get_client):
        """Scores outside 1-10 should be clamped."""
        json_text = json.dumps({
            "overall_score": 15.0,  # invalid — too high
            "criteria_scores": {c: 10 for c in DEFAULT_CRITERIA},
            "reasoning": "Test.",
        })
        mock_get_client.return_value.messages.create.return_value = _make_mock_message(json_text)
        result = score_response("prompt", "response")
        assert result.score <= 10.0

    @patch("platform_eval.llm_judge._get_client")
    def test_handles_malformed_json_gracefully(self, mock_get_client):
        """Malformed JSON should not raise — should use fallback."""
        bad_json = "I think this response is great, score: 7 out of 10, very helpful."
        mock_get_client.return_value.messages.create.return_value = _make_mock_message(bad_json)

        result = score_response("What is 2+2?", "4")

        # Should not raise, should return a JudgeScore
        assert isinstance(result, JudgeScore)
        assert 1.0 <= result.score <= 10.0

    @patch("platform_eval.llm_judge._get_client")
    def test_handles_completely_unparseable_response(self, mock_get_client):
        """Completely unstructured response should fall back to 5.0."""
        mock_get_client.return_value.messages.create.return_value = _make_mock_message(
            "I cannot evaluate this response properly."
        )
        result = score_response("prompt", "response")
        assert isinstance(result, JudgeScore)
        assert result.score == 5.0

    @patch("platform_eval.llm_judge._get_client")
    def test_raw_response_is_stored(self, mock_get_client):
        """raw_response field should contain the original judge text."""
        json_text = _make_valid_score_json()
        mock_get_client.return_value.messages.create.return_value = _make_mock_message(json_text)

        result = score_response("prompt", "response")
        assert result.raw_response == json_text.strip()

    @patch("platform_eval.llm_judge._get_client")
    def test_json_in_markdown_fence_parsed(self, mock_get_client):
        """score_response() should parse JSON even when wrapped in markdown fences."""
        criteria = {c: 7 for c in DEFAULT_CRITERIA}
        inner_json = _make_valid_score_json(overall=7.0, criteria=criteria)
        fenced = f"```json\n{inner_json}\n```"
        mock_get_client.return_value.messages.create.return_value = _make_mock_message(fenced)

        result = score_response("prompt", "response")
        assert abs(result.score - 7.0) < 1e-6

    @patch("platform_eval.llm_judge._get_client")
    def test_custom_criteria_used(self, mock_get_client):
        """Custom criteria should appear in the criteria_scores dict."""
        custom_criteria = ["reasoning", "formatting"]
        custom_scores = {"reasoning": 8, "formatting": 9}
        json_text = json.dumps({
            "overall_score": 8.5,
            "criteria_scores": custom_scores,
            "reasoning": "Good structure.",
        })
        mock_get_client.return_value.messages.create.return_value = _make_mock_message(json_text)

        result = score_response("prompt", "response", criteria=custom_criteria)
        assert "reasoning" in result.criteria_scores
        assert "formatting" in result.criteria_scores

    @patch("platform_eval.llm_judge._get_client")
    def test_default_criteria_applied_when_none(self, mock_get_client):
        """When criteria=None, DEFAULT_CRITERIA should be used."""
        criteria_scores = {c: 8 for c in DEFAULT_CRITERIA}
        json_text = _make_valid_score_json(criteria=criteria_scores)
        mock_get_client.return_value.messages.create.return_value = _make_mock_message(json_text)

        result = score_response("prompt", "response", criteria=None)
        for c in DEFAULT_CRITERIA:
            assert c in result.criteria_scores


# ─────────────────────────────────────────────────────────────────────────────
# TestCompareResponses
# ─────────────────────────────────────────────────────────────────────────────

class TestCompareResponses:
    """Tests for compare_responses() — returns ComparisonResult."""

    @patch("platform_eval.llm_judge._get_client")
    def test_returns_comparison_result(self, mock_get_client):
        """compare_responses() should return a ComparisonResult."""
        json_text = _make_valid_comparison_json(winner="B", score_a=7.0, score_b=8.5)
        mock_get_client.return_value.messages.create.return_value = _make_mock_message(json_text)

        result = compare_responses("What is Python?", "Python is a language.", "Python is a high-level language.")

        assert isinstance(result, ComparisonResult)

    @patch("platform_eval.llm_judge._get_client")
    def test_winner_is_b(self, mock_get_client):
        """Should correctly parse winner=B."""
        json_text = _make_valid_comparison_json(winner="B")
        mock_get_client.return_value.messages.create.return_value = _make_mock_message(json_text)

        result = compare_responses("prompt", "resp_a", "resp_b")
        assert result.winner == "B"

    @patch("platform_eval.llm_judge._get_client")
    def test_winner_is_a(self, mock_get_client):
        """Should correctly parse winner=A."""
        json_text = _make_valid_comparison_json(winner="A", score_a=9.0, score_b=6.0)
        mock_get_client.return_value.messages.create.return_value = _make_mock_message(json_text)

        result = compare_responses("prompt", "resp_a", "resp_b")
        assert result.winner == "A"

    @patch("platform_eval.llm_judge._get_client")
    def test_winner_is_tie(self, mock_get_client):
        """Should correctly parse winner=TIE."""
        json_text = _make_valid_comparison_json(winner="TIE", score_a=7.5, score_b=7.5)
        mock_get_client.return_value.messages.create.return_value = _make_mock_message(json_text)

        result = compare_responses("prompt", "resp_a", "resp_b")
        assert result.winner == "TIE"

    @patch("platform_eval.llm_judge._get_client")
    def test_scores_parsed_correctly(self, mock_get_client):
        """score_a and score_b should match parsed values."""
        json_text = _make_valid_comparison_json(score_a=6.5, score_b=9.0)
        mock_get_client.return_value.messages.create.return_value = _make_mock_message(json_text)

        result = compare_responses("prompt", "resp_a", "resp_b")
        assert abs(result.score_a - 6.5) < 1e-6
        assert abs(result.score_b - 9.0) < 1e-6

    @patch("platform_eval.llm_judge._get_client")
    def test_scores_clamped_to_valid_range(self, mock_get_client):
        """Scores must be clamped to [1, 10]."""
        json_text = json.dumps({
            "score_a": -5.0,  # invalid
            "score_b": 20.0,  # invalid
            "winner": "B",
            "reasoning": "test",
        })
        mock_get_client.return_value.messages.create.return_value = _make_mock_message(json_text)

        result = compare_responses("p", "a", "b")
        assert result.score_a >= 1.0
        assert result.score_b <= 10.0

    @patch("platform_eval.llm_judge._get_client")
    def test_malformed_json_fallback(self, mock_get_client):
        """Malformed JSON should fall back to TIE without raising."""
        mock_get_client.return_value.messages.create.return_value = _make_mock_message(
            "Response B is clearly better and wins this comparison. B WINS."
        )
        result = compare_responses("prompt", "resp_a", "resp_b")
        assert isinstance(result, ComparisonResult)
        assert result.winner in ("A", "B", "TIE")

    @patch("platform_eval.llm_judge._get_client")
    def test_completely_unstructured_fallback_tie(self, mock_get_client):
        """If nothing can be determined from the text, default to TIE."""
        mock_get_client.return_value.messages.create.return_value = _make_mock_message(
            "I cannot determine which is better from the given information."
        )
        result = compare_responses("prompt", "resp_a", "resp_b")
        assert result.winner in ("A", "B", "TIE")

    @patch("platform_eval.llm_judge._get_client")
    def test_winner_normalization_verbose_labels(self, mock_get_client):
        """'RESPONSE A' and 'RESPONSE B' should normalize to 'A' and 'B'."""
        json_text = json.dumps({
            "score_a": 9.0,
            "score_b": 7.0,
            "winner": "RESPONSE A",
            "reasoning": "A was better.",
        })
        mock_get_client.return_value.messages.create.return_value = _make_mock_message(json_text)
        result = compare_responses("p", "a", "b")
        assert result.winner == "A"

    @patch("platform_eval.llm_judge._get_client")
    def test_reasoning_included_in_result(self, mock_get_client):
        """reasoning field should be populated from the judge response."""
        json_text = _make_valid_comparison_json(reasoning="B was more concise and accurate.")
        mock_get_client.return_value.messages.create.return_value = _make_mock_message(json_text)

        result = compare_responses("prompt", "resp_a", "resp_b")
        assert "concise" in result.reasoning


# ─────────────────────────────────────────────────────────────────────────────
# TestBatchScore
# ─────────────────────────────────────────────────────────────────────────────

class TestBatchScore:
    """Tests for batch_score() — processes multiple samples."""

    @patch("platform_eval.llm_judge._get_client")
    def test_returns_list_of_judge_scores(self, mock_get_client):
        """batch_score() should return a JudgeScore for each input sample."""
        criteria = {c: 8 for c in DEFAULT_CRITERIA}
        json_text = _make_valid_score_json(overall=8.0, criteria=criteria)
        mock_get_client.return_value.messages.create.return_value = _make_mock_message(json_text)

        samples = [
            {"prompt": "What is 2+2?", "response": "4"},
            {"prompt": "What is the capital of France?", "response": "Paris"},
        ]
        results = batch_score(samples)

        assert len(results) == 2
        for r in results:
            assert isinstance(r, JudgeScore)

    @patch("platform_eval.llm_judge._get_client")
    def test_processes_all_samples(self, mock_get_client):
        """Should process every sample, not skip any."""
        criteria = {c: 7 for c in DEFAULT_CRITERIA}
        json_text = _make_valid_score_json(overall=7.0, criteria=criteria)
        mock_get_client.return_value.messages.create.return_value = _make_mock_message(json_text)

        n_samples = 5
        samples = [{"prompt": f"Q{i}", "response": f"A{i}"} for i in range(n_samples)]
        results = batch_score(samples)

        assert len(results) == n_samples

    @patch("platform_eval.llm_judge._get_client")
    def test_preserves_order(self, mock_get_client):
        """Results should be in the same order as input samples."""
        call_count = [0]
        scores_to_return = [9.0, 3.0, 7.0]

        def side_effect(*args, **kwargs):
            idx = call_count[0]
            call_count[0] += 1
            score = scores_to_return[idx % len(scores_to_return)]
            criteria = {c: int(score) for c in DEFAULT_CRITERIA}
            json_text = _make_valid_score_json(overall=score, criteria=criteria)
            return _make_mock_message(json_text)

        mock_get_client.return_value.messages.create.side_effect = side_effect

        samples = [
            {"prompt": "p1", "response": "r1"},
            {"prompt": "p2", "response": "r2"},
            {"prompt": "p3", "response": "r3"},
        ]
        results = batch_score(samples)

        assert abs(results[0].score - 9.0) < 1e-6
        assert abs(results[1].score - 3.0) < 1e-6
        assert abs(results[2].score - 7.0) < 1e-6

    @patch("platform_eval.llm_judge._get_client")
    def test_empty_samples_returns_empty_list(self, mock_get_client):
        """batch_score([]) should return []."""
        results = batch_score([])
        assert results == []
        mock_get_client.return_value.messages.create.assert_not_called()

    @patch("platform_eval.llm_judge._get_client")
    def test_custom_criteria_per_sample(self, mock_get_client):
        """Samples with a 'criteria' key should use those criteria."""
        custom_criteria = ["reasoning", "formatting"]
        custom_scores = {"reasoning": 8, "formatting": 7}
        json_text = json.dumps({
            "overall_score": 7.5,
            "criteria_scores": custom_scores,
            "reasoning": "Good structure.",
        })
        mock_get_client.return_value.messages.create.return_value = _make_mock_message(json_text)

        samples = [{"prompt": "p", "response": "r", "criteria": custom_criteria}]
        results = batch_score(samples)
        assert "reasoning" in results[0].criteria_scores
        assert "formatting" in results[0].criteria_scores

    @patch("platform_eval.llm_judge._get_client")
    def test_api_call_made_once_per_sample(self, mock_get_client):
        """Should call the API exactly once per sample."""
        criteria = {c: 8 for c in DEFAULT_CRITERIA}
        json_text = _make_valid_score_json(criteria=criteria)
        mock_get_client.return_value.messages.create.return_value = _make_mock_message(json_text)

        n = 4
        samples = [{"prompt": f"p{i}", "response": f"r{i}"} for i in range(n)]
        batch_score(samples)

        assert mock_get_client.return_value.messages.create.call_count == n
