"""
ab_testing/experiment.py — A/B experiment framework for comparing two LLM models.

HOW A/B TESTING WORKS FOR LLMs
================================
Traditional A/B testing (as used in web product experiments) randomly assigns
users to two variants and measures a downstream metric (click rate, conversion, etc.).

For LLM evaluation, we adapt this approach:
  - "Variant A" = Model A (Haiku: cheap, fast)
  - "Variant B" = Model B (Sonnet: more capable)
  - The "metric" = quality score from an LLM judge
  - Each "user session" = one prompt run through both models

This gives us a controlled comparison where the ONLY variable is the model.
The same prompts go to both models, eliminating prompt variation as a confounder.

RECOMMENDATION LOGIC
=====================
After running N samples:
  1. Count wins for each model (tie = neither wins)
  2. If either model has > 60% win rate → recommend that model
  3. If wins are close (between 40-60%) → INCONCLUSIVE, collect more data
  4. Cost is a tiebreaker: if quality is close but one model is >40% cheaper,
     prefer the cheaper model
"""

import os
import sys
import time
import uuid
from dataclasses import dataclass, field
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import provider as prov
import config
from config import TOKEN_PRICING, EXPERIMENT_SAMPLE_SIZE, VERBOSE
from platform_eval.llm_judge import compare_responses


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class ExperimentSample:
    """
    Results for a single prompt in an A/B experiment.

    Attributes:
        sample_id: Unique ID for this sample
        prompt: The input prompt used for both models
        model_a_response: Full text response from Model A
        model_b_response: Full text response from Model B
        model_a_cost: USD cost of Model A's response
        model_b_cost: USD cost of Model B's response
        model_a_latency_ms: Response time for Model A in milliseconds
        model_b_latency_ms: Response time for Model B in milliseconds
        judge_winner: "A", "B", or "TIE" — the judge's verdict
        judge_score_a: LLM judge quality score for Model A (1-10)
        judge_score_b: LLM judge quality score for Model B (1-10)
        judge_reasoning: Judge's explanation of its decision
    """
    sample_id: str
    prompt: str
    model_a_response: str
    model_b_response: str
    model_a_cost: float
    model_b_cost: float
    model_a_latency_ms: float
    model_b_latency_ms: float
    judge_winner: str
    judge_score_a: float
    judge_score_b: float
    judge_reasoning: str


@dataclass
class ExperimentResult:
    """
    Aggregated results from a full A/B experiment.

    Attributes:
        experiment_id: Unique ID for this experiment run
        prompts_tested: Total number of prompts evaluated
        model_a_wins: Number of samples where judge picked Model A
        model_b_wins: Number of samples where judge picked Model B
        ties: Number of samples with no clear winner
        model_a_avg_cost: Mean cost per call for Model A (USD)
        model_b_avg_cost: Mean cost per call for Model B (USD)
        model_a_avg_latency_ms: Mean latency for Model A
        model_b_avg_latency_ms: Mean latency for Model B
        model_a_avg_score: Mean judge quality score for Model A
        model_b_avg_score: Mean judge quality score for Model B
        recommendation: "USE_A", "USE_B", or "INCONCLUSIVE"
        samples: Full list of ExperimentSample objects
    """
    experiment_id: str
    prompts_tested: int
    model_a_wins: int
    model_b_wins: int
    ties: int
    model_a_avg_cost: float
    model_b_avg_cost: float
    model_a_avg_latency_ms: float
    model_b_avg_latency_ms: float
    model_a_avg_score: float
    model_b_avg_score: float
    recommendation: str
    samples: list[ExperimentSample] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _call_model(model: str, prompt: str) -> tuple[str, float, int, int]:
    """
    Call the specified model and return (response_text, latency_ms, input_tokens, output_tokens).

    Returns ("", elapsed_ms, 0, 0) on any API error so the experiment
    can continue even if individual calls fail.
    """
    api_key = (
        config.ANTHROPIC_API_KEY if config.PROVIDER == "anthropic" else config.OPENAI_API_KEY
    ) or os.environ.get(
        "ANTHROPIC_API_KEY" if config.PROVIDER == "anthropic" else "OPENAI_API_KEY", ""
    )
    client = prov.create_client(config.PROVIDER or "anthropic", api_key)

    start = time.perf_counter()
    try:
        response = prov.call_api(
            client=client,
            provider=config.PROVIDER or "anthropic",
            model=model,
            max_tokens=1024,
            system="You are a helpful assistant.",
            tools=None,
            messages=[{"role": "user", "content": prompt}],
        )
        elapsed_ms = (time.perf_counter() - start) * 1000.0
        text = response.content[0]["text"].strip() if response.content else ""
        return text, elapsed_ms, response.usage.input_tokens, response.usage.output_tokens
    except Exception as e:
        elapsed_ms = (time.perf_counter() - start) * 1000.0
        if VERBOSE:
            print(f"[Experiment ERROR] Model call failed ({model}): {e}")
        return "", elapsed_ms, 0, 0


def _compute_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    """Compute USD cost from token counts."""
    pricing = TOKEN_PRICING.get(model, {"input": 0.0, "output": 0.0})
    return (input_tokens / 1_000_000) * pricing["input"] + \
           (output_tokens / 1_000_000) * pricing["output"]


def _determine_recommendation(
    wins_a: int,
    wins_b: int,
    ties: int,
    avg_cost_a: float,
    avg_cost_b: float,
    avg_score_a: float,
    avg_score_b: float,
) -> str:
    """
    Determine the recommendation based on win rates and cost/quality tradeoffs.

    Decision logic:
    1. Clear quality winner (>60% win rate, excluding ties): prefer that model
    2. If quality is close (within 0.5 points) and one model is 40%+ cheaper: prefer cheaper
    3. Otherwise: INCONCLUSIVE — need more data or human judgment

    Returns:
        "USE_A", "USE_B", or "INCONCLUSIVE"
    """
    total_compared = wins_a + wins_b
    if total_compared == 0:
        return "INCONCLUSIVE"

    win_rate_a = wins_a / total_compared
    win_rate_b = wins_b / total_compared

    # Clear quality winner threshold: 60%
    if win_rate_b >= 0.60:
        return "USE_B"
    if win_rate_a >= 0.60:
        return "USE_A"

    # Quality is close — use cost as tiebreaker
    quality_diff = abs(avg_score_b - avg_score_a)
    if quality_diff < 0.5 and avg_cost_a > 0 and avg_cost_b > 0:
        cost_ratio = avg_cost_b / avg_cost_a
        if cost_ratio > 1.4:
            # B is significantly more expensive with similar quality → use A
            return "USE_A"
        if cost_ratio < (1.0 / 1.4):
            # B is significantly cheaper with similar quality → use B
            return "USE_B"

    return "INCONCLUSIVE"


# ---------------------------------------------------------------------------
# Main experiment runner
# ---------------------------------------------------------------------------

def run_experiment(
    prompts: list[str],
    experiment_id: Optional[str] = None,
) -> ExperimentResult:
    """
    Run an A/B experiment comparing MODEL_A and MODEL_B on a set of prompts.

    For each prompt:
      1. Call MODEL_A → record response, cost, and latency
      2. Call MODEL_B → record response, cost, and latency
      3. Ask LLM judge to compare the two responses → record winner and scores
      4. Aggregate all samples into an ExperimentResult

    The recommendation is determined by:
      - Win rate (>60% = clear winner)
      - Cost as a tiebreaker when quality is similar

    Args:
        prompts: List of prompt strings to test. Should be representative of
                 your actual production traffic for the most meaningful results.
        experiment_id: Optional unique ID. Auto-generated if not provided.

    Returns:
        ExperimentResult with full details and a recommendation.

    Example:
        prompts = [
            "Summarize this article in 3 bullet points: ...",
            "What are the pros and cons of remote work?",
            # ... more prompts
        ]
        result = run_experiment(prompts, experiment_id="summarization-v2-test")
        print(result.recommendation)
        print_analysis(result)  # from statistical_analysis module
    """
    if experiment_id is None:
        experiment_id = f"exp-{uuid.uuid4().hex[:8]}"

    if VERBOSE:
        print(f"[Experiment] Starting '{experiment_id}' with {len(prompts)} prompts")
        model_a = config.MODEL_A if config.PROVIDER == "anthropic" else config.MODEL_A_OPENAI
        model_b = config.MODEL_B if config.PROVIDER == "anthropic" else config.MODEL_B_OPENAI
        print(f"  Model A: {model_a}")
        print(f"  Model B: {model_b}")

    samples: list[ExperimentSample] = []
    wins_a = 0
    wins_b = 0
    ties = 0

    costs_a: list[float] = []
    costs_b: list[float] = []
    latencies_a: list[float] = []
    latencies_b: list[float] = []
    scores_a: list[float] = []
    scores_b: list[float] = []

    total = len(prompts)

    for i, prompt in enumerate(prompts):
        sample_id = f"{experiment_id}-s{i+1:03d}"

        if VERBOSE:
            print(f"[Experiment] Sample {i+1}/{total}: {prompt[:60]}{'...' if len(prompt) > 60 else ''}")

        model_a = config.MODEL_A if config.PROVIDER == "anthropic" else config.MODEL_A_OPENAI
        model_b = config.MODEL_B if config.PROVIDER == "anthropic" else config.MODEL_B_OPENAI

        # Step 1: Call Model A
        response_a, latency_a, in_tokens_a, out_tokens_a = _call_model(model_a, prompt)
        cost_a = _compute_cost(model_a, in_tokens_a, out_tokens_a)

        # Step 2: Call Model B
        response_b, latency_b, in_tokens_b, out_tokens_b = _call_model(model_b, prompt)
        cost_b = _compute_cost(model_b, in_tokens_b, out_tokens_b)

        # Step 3: Judge comparison
        winner = "TIE"
        score_a_val = 5.0
        score_b_val = 5.0
        reasoning = ""

        if response_a and response_b:
            try:
                comparison = compare_responses(prompt, response_a, response_b)
                winner = comparison.winner
                score_a_val = comparison.score_a
                score_b_val = comparison.score_b
                reasoning = comparison.reasoning
            except Exception as e:
                if VERBOSE:
                    print(f"  [Experiment] Judge failed for sample {i+1}: {e}")
                winner = "TIE"
        elif not response_a and not response_b:
            winner = "TIE"
        elif not response_a:
            winner = "B"
            score_b_val = 7.0
        else:
            winner = "A"
            score_a_val = 7.0

        # Tally wins
        if winner == "A":
            wins_a += 1
        elif winner == "B":
            wins_b += 1
        else:
            ties += 1

        # Accumulate metrics
        costs_a.append(cost_a)
        costs_b.append(cost_b)
        latencies_a.append(latency_a)
        latencies_b.append(latency_b)
        scores_a.append(score_a_val)
        scores_b.append(score_b_val)

        sample = ExperimentSample(
            sample_id=sample_id,
            prompt=prompt,
            model_a_response=response_a,
            model_b_response=response_b,
            model_a_cost=cost_a,
            model_b_cost=cost_b,
            model_a_latency_ms=latency_a,
            model_b_latency_ms=latency_b,
            judge_winner=winner,
            judge_score_a=score_a_val,
            judge_score_b=score_b_val,
            judge_reasoning=reasoning,
        )
        samples.append(sample)

        if VERBOSE:
            print(f"  Winner: {winner} | Score A={score_a_val:.1f} B={score_b_val:.1f} | "
                  f"Cost A=${cost_a:.5f} B=${cost_b:.5f}")

    # Aggregate
    n = len(samples)
    avg_cost_a = sum(costs_a) / n if n > 0 else 0.0
    avg_cost_b = sum(costs_b) / n if n > 0 else 0.0
    avg_latency_a = sum(latencies_a) / n if n > 0 else 0.0
    avg_latency_b = sum(latencies_b) / n if n > 0 else 0.0
    avg_score_a = sum(scores_a) / n if n > 0 else 0.0
    avg_score_b = sum(scores_b) / n if n > 0 else 0.0

    recommendation = _determine_recommendation(
        wins_a, wins_b, ties,
        avg_cost_a, avg_cost_b,
        avg_score_a, avg_score_b,
    )

    result = ExperimentResult(
        experiment_id=experiment_id,
        prompts_tested=n,
        model_a_wins=wins_a,
        model_b_wins=wins_b,
        ties=ties,
        model_a_avg_cost=round(avg_cost_a, 8),
        model_b_avg_cost=round(avg_cost_b, 8),
        model_a_avg_latency_ms=round(avg_latency_a, 2),
        model_b_avg_latency_ms=round(avg_latency_b, 2),
        model_a_avg_score=round(avg_score_a, 3),
        model_b_avg_score=round(avg_score_b, 3),
        recommendation=recommendation,
        samples=samples,
    )

    if VERBOSE:
        print(f"\n[Experiment] Complete: A={wins_a} wins, B={wins_b} wins, {ties} ties")
        print(f"[Experiment] Recommendation: {recommendation}")

    return result
