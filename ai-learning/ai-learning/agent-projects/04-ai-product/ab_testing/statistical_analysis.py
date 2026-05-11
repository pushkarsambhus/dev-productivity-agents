"""
ab_testing/statistical_analysis.py — Statistical tools for A/B experiment analysis.

STATISTICS WITHOUT SCIPY
==========================
This module implements all statistics using Python's built-in `math` and
`statistics` modules only — no numpy, no scipy. This makes the code easier
to understand and deploy in environments with minimal dependencies.

KEY CONCEPTS FOR PM/EM/TPM AUDIENCES
======================================

Win Rate
─────────
The simplest metric: what fraction of the time did Model B beat Model A?
A win rate of 0.60 means Model B won 60% of head-to-head comparisons.
BUT: a win rate calculated on 5 samples is nearly meaningless — you need
confidence intervals to know if the result is real.

Wilson Score Confidence Interval
──────────────────────────────────
A confidence interval tells you the range within which the true win rate
probably falls. For small samples, the Wilson score interval is more accurate
than the naive (p ± 1.96*SE) interval.

Example:
  5 wins out of 10 trials → naive CI: [0.19, 0.81] → very wide, don't conclude anything
  15 wins out of 20 trials → CI: [0.54, 0.87] → lower bound > 0.5, Model B probably better

Statistical Significance (binomial test)
─────────────────────────────────────────
Is Model B's win rate statistically distinguishable from a 50/50 coin flip?
We use a two-sided binomial test with alpha=0.05. If the p-value < 0.05,
we can say "the difference is statistically significant."

Caveat: With N=20 samples, you need at least 15 wins (or 15 losses) to
reach significance. This is why EXPERIMENT_SAMPLE_SIZE matters.

Effect Size (Cohen's d)
────────────────────────
Statistical significance tells you IF a difference exists. Effect size tells
you HOW BIG it is. Cohen's d < 0.2 is "trivial", 0.2-0.5 is "small",
0.5-0.8 is "medium", > 0.8 is "large."

You might have a statistically significant result with d=0.1 — technically
real, but probably not worth the cost premium of a more expensive model.

Cost-Quality Tradeoff
─────────────────────
The ultimate PM decision: Is the quality gain worth the extra cost?
We express this as "quality gained per dollar spent" — similar to ROI.
"""

import math
import statistics
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ab_testing.experiment import ExperimentResult


# ---------------------------------------------------------------------------
# Basic win rate
# ---------------------------------------------------------------------------

def win_rate(wins: int, total: int) -> float:
    """
    Compute the simple win rate as a fraction.

    Args:
        wins: Number of wins for one model
        total: Total number of comparisons

    Returns:
        Float between 0.0 and 1.0, or 0.0 if total is 0.

    Example:
        win_rate(12, 20) → 0.6  # Model won 60% of comparisons
    """
    if total == 0:
        return 0.0
    return wins / total


# ---------------------------------------------------------------------------
# Wilson score confidence interval (no scipy needed)
# ---------------------------------------------------------------------------

def confidence_interval(
    wins: int,
    total: int,
    confidence: float = 0.95,
) -> tuple[float, float]:
    """
    Compute the Wilson score confidence interval for a proportion.

    The Wilson interval is more accurate than the normal approximation,
    especially for small samples (N < 30) or extreme proportions (near 0 or 1).

    The formula is:
        center = (wins + z²/2) / (total + z²)
        margin = z * sqrt(wins*(total-wins)/total + z²/4) / (total + z²)
        CI = (center - margin, center + margin)

    Args:
        wins: Number of successes
        total: Number of trials
        confidence: Confidence level, e.g. 0.95 for 95% CI

    Returns:
        (lower_bound, upper_bound) tuple, both in [0, 1].

    Examples:
        confidence_interval(5, 10)   → approximately (0.24, 0.76)  → inconclusive
        confidence_interval(15, 20)  → approximately (0.54, 0.87)  → B probably better
        confidence_interval(19, 20)  → approximately (0.73, 0.99)  → B clearly better
    """
    if total == 0:
        return (0.0, 1.0)

    # z-score for the given confidence level (two-tailed)
    # Common values: 0.90→1.645, 0.95→1.960, 0.99→2.576
    alpha = 1.0 - confidence
    z = _z_score(1.0 - alpha / 2.0)

    p_hat = wins / total
    n = total
    z2 = z * z

    # Wilson score formula
    denominator = 1.0 + z2 / n
    center = (p_hat + z2 / (2 * n)) / denominator
    margin = (z / denominator) * math.sqrt(
        p_hat * (1.0 - p_hat) / n + z2 / (4 * n * n)
    )

    lower = max(0.0, center - margin)
    upper = min(1.0, center + margin)
    return (lower, upper)


def _z_score(p: float) -> float:
    """
    Inverse normal CDF approximation using the Beasley-Springer-Moro algorithm.
    Returns the z-score for which P(Z <= z) = p.

    This is accurate to ~5 decimal places for p in (0.0001, 0.9999).
    """
    if p <= 0.0:
        return -float("inf")
    if p >= 1.0:
        return float("inf")
    if p == 0.5:
        return 0.0

    # Coefficients for rational approximation
    a = [
        -3.969683028665376e+01,
         2.209460984245205e+02,
        -2.759285104469687e+02,
         1.383577518672690e+02,
        -3.066479806614716e+01,
         2.506628277459239e+00,
    ]
    b = [
        -5.447609879822406e+01,
         1.615858368580409e+02,
        -1.556989798598866e+02,
         6.680131188771972e+01,
        -1.328068155288572e+01,
    ]
    c = [
        -7.784894002430293e-03,
        -3.223964580411365e-01,
        -2.400758277161838e+00,
        -2.549732539343734e+00,
         4.374664141464968e+00,
         2.938163982698783e+00,
    ]
    d = [
         7.784695709041462e-03,
         3.224671290700398e-01,
         2.445134137142996e+00,
         3.754408661907416e+00,
    ]

    p_low = 0.02425
    p_high = 1.0 - p_low

    if p < p_low:
        # Rational approximation for lower region
        q = math.sqrt(-2.0 * math.log(p))
        result = (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / \
                 ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1.0)
    elif p <= p_high:
        # Rational approximation for central region
        q = p - 0.5
        r = q * q
        result = (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q / \
                 (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1.0)
    else:
        # Rational approximation for upper region
        q = math.sqrt(-2.0 * math.log(1.0 - p))
        result = -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / \
                  ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1.0)

    return result


# ---------------------------------------------------------------------------
# Statistical significance (two-sided binomial test)
# ---------------------------------------------------------------------------

def is_significant(
    wins_a: int,
    wins_b: int,
    alpha: float = 0.05,
) -> bool:
    """
    Test whether one model significantly outperforms the other.

    Uses a two-sided binomial test: under H0 (no difference), each
    comparison is a fair coin flip (p=0.5). We compute the probability
    of seeing the observed or more extreme distribution.

    Args:
        wins_a: Number of comparisons won by Model A
        wins_b: Number of comparisons won by Model B
        alpha: Significance threshold (default 0.05 = 5%)

    Returns:
        True if the result is statistically significant at level alpha.
        False if the result could reasonably be due to chance.

    Interpretation:
        True  → "Model B (or A) is significantly better — we can reject the null."
        False → "The difference could be random — collect more data."

    Note: Ties are excluded from this test. Only wins_a + wins_b are the
    effective trial count (assuming ties indicate no preference).
    """
    total = wins_a + wins_b
    if total == 0:
        return False

    # The winning model's count
    k = max(wins_a, wins_b)  # observed wins for the "winner"
    n = total
    p = 0.5  # null hypothesis probability

    # Compute exact binomial p-value (two-sided)
    # p_value = 2 * P(X >= k) where X ~ Binomial(n, 0.5)
    # P(X >= k) = sum_{i=k}^{n} C(n,i) * 0.5^n
    p_value = 2.0 * _binomial_tail(n, k, p)
    # Cap at 1.0 for two-sided test
    p_value = min(1.0, p_value)

    return p_value < alpha


def _binomial_coeff(n: int, k: int) -> float:
    """Compute binomial coefficient C(n, k) using log-gamma for numerical stability."""
    if k < 0 or k > n:
        return 0.0
    if k == 0 or k == n:
        return 1.0
    return math.exp(
        math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)
    )


def _binomial_tail(n: int, k: int, p: float) -> float:
    """
    Compute P(X >= k) for X ~ Binomial(n, p).
    Returns sum of P(X = i) for i from k to n.
    """
    # For p=0.5, P(X=i) = C(n,i) * 0.5^n
    total_prob = 0.0
    log_half_n = n * math.log(0.5)  # log(0.5^n)

    for i in range(k, n + 1):
        log_prob = math.lgamma(n + 1) - math.lgamma(i + 1) - math.lgamma(n - i + 1) + log_half_n
        total_prob += math.exp(log_prob)

    return total_prob


# ---------------------------------------------------------------------------
# Effect size (Cohen's d)
# ---------------------------------------------------------------------------

def effect_size(score_a: list[float], score_b: list[float]) -> float:
    """
    Compute Cohen's d effect size between two score distributions.

    Cohen's d = (mean_B - mean_A) / pooled_std_dev

    Interpretation:
        |d| < 0.2  → negligible (the difference is tiny)
        |d| 0.2-0.5 → small
        |d| 0.5-0.8 → medium (practically meaningful)
        |d| > 0.8  → large (very meaningful)

    Positive d means Model B scored higher on average.

    Args:
        score_a: List of quality scores for Model A (1-10 from LLM judge)
        score_b: List of quality scores for Model B (1-10 from LLM judge)

    Returns:
        Cohen's d as a float. Returns 0.0 if either list is empty or has
        zero variance (all scores identical).
    """
    if len(score_a) < 2 or len(score_b) < 2:
        return 0.0

    mean_a = statistics.mean(score_a)
    mean_b = statistics.mean(score_b)

    var_a = statistics.variance(score_a)
    var_b = statistics.variance(score_b)

    n_a = len(score_a)
    n_b = len(score_b)

    # Pooled standard deviation (weighted by sample size)
    pooled_var = ((n_a - 1) * var_a + (n_b - 1) * var_b) / (n_a + n_b - 2)
    pooled_std = math.sqrt(pooled_var)

    if pooled_std == 0.0:
        return 0.0

    return (mean_b - mean_a) / pooled_std


# ---------------------------------------------------------------------------
# Cost-quality tradeoff
# ---------------------------------------------------------------------------

def cost_quality_tradeoff(
    cost_a: float,
    quality_a: float,
    cost_b: float,
    quality_b: float,
) -> str:
    """
    Generate a human-readable recommendation based on cost and quality.

    This function computes quality-per-dollar for each model and returns
    a plain-English recommendation suitable for stakeholder reports.

    Args:
        cost_a: Average cost per call for Model A (USD)
        quality_a: Average quality score for Model A (1-10)
        cost_b: Average cost per call for Model B (USD)
        quality_b: Average quality score for Model B (1-10)

    Returns:
        Human-readable recommendation string.

    Example outputs:
        "Model A is both cheaper and better — prefer Model A."
        "Model B is 2.3x better quality at 4.1x the cost. The quality premium may be worth it."
        "Quality difference is negligible (0.3 pts). Use Model A for cost savings."
    """
    quality_delta = quality_b - quality_a
    cost_ratio = cost_b / cost_a if cost_a > 0 else float("inf")

    # Case 1: A dominates on both dimensions
    if quality_a >= quality_b and cost_a <= cost_b:
        return (
            f"Model A is both cheaper (${cost_a:.4f} vs ${cost_b:.4f}) "
            f"and equal or better quality ({quality_a:.1f} vs {quality_b:.1f}). "
            f"Prefer Model A."
        )

    # Case 2: B dominates on both dimensions
    if quality_b > quality_a and cost_b <= cost_a:
        return (
            f"Model B is both cheaper (${cost_b:.4f} vs ${cost_a:.4f}) "
            f"and better quality ({quality_b:.1f} vs {quality_a:.1f}). "
            f"Prefer Model B."
        )

    # Case 3: Quality difference is negligible (< 0.5 points)
    if abs(quality_delta) < 0.5:
        cheaper = "A" if cost_a <= cost_b else "B"
        cheaper_cost = cost_a if cost_a <= cost_b else cost_b
        return (
            f"Quality difference is negligible ({abs(quality_delta):.1f} pts). "
            f"Model {cheaper} (${cheaper_cost:.4f}/call) offers better cost efficiency. "
            f"Use Model {cheaper} unless specific tasks require the other."
        )

    # Case 4: B is better quality but more expensive
    if quality_b > quality_a and cost_b > cost_a:
        quality_gain_pct = (quality_b - quality_a) / quality_a * 100
        qpd_a = quality_a / cost_a if cost_a > 0 else float("inf")
        qpd_b = quality_b / cost_b if cost_b > 0 else float("inf")

        if qpd_b >= qpd_a:
            verdict = "Model B offers better quality-per-dollar despite higher absolute cost."
        elif cost_ratio > 3.0 and quality_delta < 1.0:
            verdict = (
                f"Model B costs {cost_ratio:.1f}x more but improves quality by only "
                f"{quality_delta:.1f} pts. Unless quality is critical, Model A is more cost-efficient."
            )
        else:
            verdict = (
                f"Model B improves quality by {quality_delta:.1f} pts (+{quality_gain_pct:.0f}%) "
                f"at {cost_ratio:.1f}x the cost. Consider your quality-cost priorities."
            )

        return (
            f"Model A: ${cost_a:.4f}/call, score={quality_a:.1f}. "
            f"Model B: ${cost_b:.4f}/call, score={quality_b:.1f}. "
            f"{verdict}"
        )

    # Case 5: A is better quality but more expensive
    if quality_a > quality_b and cost_a > cost_b:
        return (
            f"Model A has higher quality ({quality_a:.1f} vs {quality_b:.1f}) "
            f"but costs more (${cost_a:.4f} vs ${cost_b:.4f}/call). "
            f"For cost-sensitive workloads, use Model B. For quality-critical tasks, use Model A."
        )

    # Fallback
    return (
        f"Model A: score={quality_a:.1f}, cost=${cost_a:.4f}. "
        f"Model B: score={quality_b:.1f}, cost=${cost_b:.4f}. "
        f"Review both metrics to determine the best fit for your use case."
    )


# ---------------------------------------------------------------------------
# Full report printer
# ---------------------------------------------------------------------------

def print_analysis(result: "ExperimentResult") -> None:
    """
    Print a complete statistical analysis of an A/B experiment result.

    Args:
        result: ExperimentResult from ab_testing.experiment.run_experiment()
    """
    sep = "=" * 65
    total_comparisons = result.model_a_wins + result.model_b_wins + result.ties

    print(f"\n{sep}")
    print(f"  A/B STATISTICAL ANALYSIS")
    print(f"  Experiment: {result.experiment_id}")
    print(sep)

    print(f"\n  RESULTS SUMMARY")
    print(f"  {'Total prompts tested:':<35} {result.prompts_tested}")
    print(f"  {'Model A wins:':<35} {result.model_a_wins}")
    print(f"  {'Model B wins:':<35} {result.model_b_wins}")
    print(f"  {'Ties:':<35} {result.ties}")

    # Win rates
    wr_a = win_rate(result.model_a_wins, total_comparisons)
    wr_b = win_rate(result.model_b_wins, total_comparisons)
    print(f"\n  WIN RATES (excluding ties)")
    head_to_head = result.model_a_wins + result.model_b_wins
    if head_to_head > 0:
        wr_a_nh = win_rate(result.model_a_wins, head_to_head)
        wr_b_nh = win_rate(result.model_b_wins, head_to_head)
        ci_a = confidence_interval(result.model_a_wins, head_to_head)
        ci_b = confidence_interval(result.model_b_wins, head_to_head)
        print(f"  Model A win rate: {wr_a_nh:.1%}  95% CI: [{ci_a[0]:.1%}, {ci_a[1]:.1%}]")
        print(f"  Model B win rate: {wr_b_nh:.1%}  95% CI: [{ci_b[0]:.1%}, {ci_b[1]:.1%}]")

        sig = is_significant(result.model_a_wins, result.model_b_wins)
        sig_str = "YES — result is statistically significant" if sig else "NO — difference may be due to chance"
        print(f"\n  {'Statistically significant?':<35} {sig_str}")

    # Quality scores
    scores_a = [s.judge_score_a for s in result.samples]
    scores_b = [s.judge_score_b for s in result.samples]
    d = effect_size(scores_a, scores_b)
    d_label = (
        "negligible" if abs(d) < 0.2 else
        "small" if abs(d) < 0.5 else
        "medium" if abs(d) < 0.8 else
        "large"
    )
    direction = "B > A" if d > 0 else "A > B" if d < 0 else "equal"

    print(f"\n  QUALITY SCORES (LLM Judge, 1-10)")
    print(f"  {'Model A avg score:':<35} {result.model_a_avg_score:.2f}")
    print(f"  {'Model B avg score:':<35} {result.model_b_avg_score:.2f}")
    print(f"  {'Effect size (Cohen\\'s d):':<35} {d:.3f} ({d_label}, {direction})")

    # Cost comparison
    print(f"\n  COST COMPARISON")
    print(f"  {'Model A avg cost per call:':<35} ${result.model_a_avg_cost:.6f}")
    print(f"  {'Model B avg cost per call:':<35} ${result.model_b_avg_cost:.6f}")
    if result.model_a_avg_cost > 0:
        ratio = result.model_b_avg_cost / result.model_a_avg_cost
        print(f"  {'Model B / Model A cost ratio:':<35} {ratio:.2f}x")

    # Latency
    print(f"\n  LATENCY COMPARISON")
    print(f"  {'Model A avg latency:':<35} {result.model_a_avg_latency_ms:.0f}ms")
    print(f"  {'Model B avg latency:':<35} {result.model_b_avg_latency_ms:.0f}ms")

    # Cost-quality tradeoff
    print(f"\n  COST-QUALITY TRADEOFF ANALYSIS")
    tradeoff = cost_quality_tradeoff(
        result.model_a_avg_cost, result.model_a_avg_score,
        result.model_b_avg_cost, result.model_b_avg_score,
    )
    # Word-wrap at 60 chars
    words = tradeoff.split(" ")
    line = "  "
    for word in words:
        if len(line) + len(word) > 65:
            print(line)
            line = "  " + word + " "
        else:
            line += word + " "
    if line.strip():
        print(line)

    # Recommendation
    print(f"\n  RECOMMENDATION: {result.recommendation}")
    print(f"\n{sep}\n")
