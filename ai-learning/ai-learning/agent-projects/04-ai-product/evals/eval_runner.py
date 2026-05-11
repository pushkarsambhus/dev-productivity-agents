"""
evals/eval_runner.py — Evaluation runner for the AI product project.

Loads eval_cases.json, runs each evaluation case against the models,
and saves results to eval_results.json.

Usage:
    # Run all eval cases (requires ANTHROPIC_API_KEY)
    python evals/eval_runner.py

    # Run a specific eval case by ID
    python evals/eval_runner.py --id quality_threshold

    # Dry-run mode: skip API calls and return mock results
    python evals/eval_runner.py --dry-run

    # Dry-run a specific case
    python evals/eval_runner.py --id cost_efficiency --dry-run

EVAL CASE TYPES
================
Each eval_case.json entry has an "id" that determines how it's evaluated:

  quality_threshold     → Run benchmark suite on all configured models, check avg score
  cost_efficiency       → Compare Haiku vs Sonnet cost on the same prompts
  sla_compliance        → Run timed API calls and check P95 latency
  regression_baseline   → Run full regression suite on Sonnet
  ab_winner_determination → Run A/B experiment, check that a recommendation was made

DRY-RUN MODE
=============
In dry-run mode, all API calls are skipped. Instead, mock results are generated
to verify the runner logic itself works correctly. This lets you test CI pipelines
without spending API budget.
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import provider as prov
import config
from config import (
    MODEL_A, MODEL_B, JUDGE_MODEL,
    SLA_LATENCY_P95_MS, MIN_QUALITY_SCORE,
    EXPERIMENT_SAMPLE_SIZE, VERBOSE,
)

# ─────────────────────────────────────────────────────────────────────────────
# Paths
# ─────────────────────────────────────────────────────────────────────────────

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
EVAL_CASES_PATH = os.path.join(_SCRIPT_DIR, "eval_cases.json")
EVAL_RESULTS_PATH = os.path.join(_SCRIPT_DIR, "eval_results.json")


# ─────────────────────────────────────────────────────────────────────────────
# Dry-run mock data generators
# ─────────────────────────────────────────────────────────────────────────────

def _mock_benchmark_results(model: str) -> list:
    """Return mock BenchmarkResult-like dicts for dry-run mode."""
    categories = ["reasoning", "factual", "coding", "safety", "instruction_following"]
    results = []
    for cat in categories:
        base_score = 7.5 if model == MODEL_B else 6.8
        results.append({
            "model": model,
            "category": cat,
            "prompts_run": 5,
            "avg_quality_score": base_score,
            "avg_cost_usd": 0.0001 if model == MODEL_A else 0.0004,
            "avg_latency_ms": 800.0 if model == MODEL_A else 1500.0,
            "pass_rate": 0.8 if model == MODEL_B else 0.7,
        })
    return results


def _mock_regression_results(model: str) -> list:
    """Return mock regression results for dry-run mode."""
    from platform_eval.regression_suite import REGRESSION_CASES
    results = []
    for case in REGRESSION_CASES:
        results.append({
            "case_id": case.case_id,
            "passed": True,
            "quality_score": 8.0,
            "failures": [],
            "response": f"[DRY RUN] Mock response for {case.case_id}",
        })
    return results


def _mock_experiment_result() -> dict:
    """Return a mock ExperimentResult-like dict for dry-run mode."""
    return {
        "experiment_id": "dry-run-exp-001",
        "prompts_tested": 10,
        "model_a_wins": 3,
        "model_b_wins": 7,
        "ties": 0,
        "model_a_avg_cost": 0.00008,
        "model_b_avg_cost": 0.00035,
        "model_a_avg_latency_ms": 750.0,
        "model_b_avg_latency_ms": 1400.0,
        "model_a_avg_score": 7.1,
        "model_b_avg_score": 8.3,
        "recommendation": "USE_B",
    }


# ─────────────────────────────────────────────────────────────────────────────
# Individual eval case runners
# ─────────────────────────────────────────────────────────────────────────────

def run_quality_threshold(case: dict, dry_run: bool) -> dict:
    """
    Check that both models meet the minimum average quality score.

    Runs the benchmark suite on each model and checks that the average
    quality score across all categories meets pass_criteria.min_avg_quality.
    """
    min_avg = case["pass_criteria"]["min_avg_quality"]
    models = case.get("models", [MODEL_A, MODEL_B])

    result = {
        "eval_id": case["id"],
        "description": case["description"],
        "pass_criteria": case["pass_criteria"],
        "model_results": {},
        "passed": True,
        "notes": [],
    }

    for model in models:
        if dry_run:
            bench_results = _mock_benchmark_results(model)
        else:
            from platform_eval.benchmark import run_benchmark
            benchmark_objs = run_benchmark(model)
            bench_results = [
                {
                    "model": r.model,
                    "category": r.category,
                    "avg_quality_score": r.avg_quality_score,
                    "pass_rate": r.pass_rate,
                }
                for r in benchmark_objs
            ]

        if bench_results:
            avg_score = sum(r["avg_quality_score"] for r in bench_results) / len(bench_results)
        else:
            avg_score = 0.0

        passed_for_model = avg_score >= min_avg
        result["model_results"][model] = {
            "avg_quality_score": round(avg_score, 3),
            "passed": passed_for_model,
        }

        if not passed_for_model:
            result["passed"] = False
            result["notes"].append(
                f"Model {model} avg score {avg_score:.2f} < required {min_avg}"
            )

    if result["passed"]:
        result["notes"].append("All models met quality threshold.")

    return result


def run_cost_efficiency(case: dict, dry_run: bool) -> dict:
    """
    Verify that Haiku is at least 50% cheaper than Sonnet on equivalent tasks.

    Runs the same set of benchmark prompts on both models and compares
    average cost per call. The pass criterion is that Haiku's cost / Sonnet's cost
    <= max_cost_ratio (default 0.5).
    """
    max_ratio = case["pass_criteria"]["max_cost_ratio"]

    result = {
        "eval_id": case["id"],
        "description": case["description"],
        "pass_criteria": case["pass_criteria"],
        "haiku_avg_cost": None,
        "sonnet_avg_cost": None,
        "actual_ratio": None,
        "passed": False,
        "notes": [],
    }

    if dry_run:
        haiku_results = _mock_benchmark_results(MODEL_A)
        sonnet_results = _mock_benchmark_results(MODEL_B)
    else:
        from platform_eval.benchmark import run_benchmark
        # Run just the "factual" category for cost comparison (5 prompts, deterministic)
        haiku_objs = run_benchmark(MODEL_A, categories=["factual"])
        sonnet_objs = run_benchmark(MODEL_B, categories=["factual"])
        haiku_results = [{"avg_cost_usd": r.avg_cost_usd} for r in haiku_objs]
        sonnet_results = [{"avg_cost_usd": r.avg_cost_usd} for r in sonnet_objs]

    haiku_avg = (
        sum(r["avg_cost_usd"] for r in haiku_results) / len(haiku_results)
        if haiku_results else 0.0
    )
    sonnet_avg = (
        sum(r["avg_cost_usd"] for r in sonnet_results) / len(sonnet_results)
        if sonnet_results else 0.0
    )

    result["haiku_avg_cost"] = round(haiku_avg, 8)
    result["sonnet_avg_cost"] = round(sonnet_avg, 8)

    if sonnet_avg > 0:
        ratio = haiku_avg / sonnet_avg
        result["actual_ratio"] = round(ratio, 4)
        if ratio <= max_ratio:
            result["passed"] = True
            result["notes"].append(
                f"Haiku is {(1 - ratio) * 100:.0f}% cheaper than Sonnet. "
                f"Cost ratio: {ratio:.3f} (required <= {max_ratio})"
            )
        else:
            result["notes"].append(
                f"Haiku/Sonnet cost ratio {ratio:.3f} exceeds max allowed {max_ratio}. "
                f"Haiku is not cheap enough relative to Sonnet for this workload."
            )
    else:
        result["notes"].append("Could not compute cost ratio — Sonnet cost was 0.")

    return result


def run_sla_compliance(case: dict, dry_run: bool) -> dict:
    """
    Check that P95 latency is under the SLA threshold.

    Makes a series of API calls to both models and measures latency,
    then checks that P95 <= max_p95_latency_ms.
    """
    max_p95 = case["pass_criteria"]["max_p95_latency_ms"]

    result = {
        "eval_id": case["id"],
        "description": case["description"],
        "pass_criteria": case["pass_criteria"],
        "model_latencies": {},
        "passed": True,
        "notes": [],
    }

    if dry_run:
        # Mock latency data: both models well within SLA
        result["model_latencies"][MODEL_A] = {
            "p50_ms": 600.0, "p95_ms": 1200.0, "passed": True
        }
        result["model_latencies"][MODEL_B] = {
            "p50_ms": 1100.0, "p95_ms": 2800.0, "passed": True
        }
        result["notes"].append("[DRY RUN] Both models within SLA threshold.")
        return result

    # Real mode: make 10 test calls and measure latency
    from tracking.latency_tracker import LatencyTracker
    import anthropic

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    client = anthropic.Anthropic(api_key=api_key)

    test_prompt = "What is 2+2? Answer in one word."
    n_calls = 10

    for model in [MODEL_A, MODEL_B]:
        tracker = LatencyTracker()
        for _ in range(n_calls):
            with tracker.measure(model, model=model):
                try:
                    client.messages.create(
                        model=model,
                        max_tokens=20,
                        messages=[{"role": "user", "content": test_prompt}],
                    )
                except Exception as e:
                    if VERBOSE:
                        print(f"[EvalRunner] SLA test call failed: {e}")

        p95 = tracker.p95()
        passed = p95 <= max_p95
        result["model_latencies"][model] = {
            "p50_ms": round(tracker.p50(), 1),
            "p95_ms": round(p95, 1),
            "passed": passed,
        }
        if not passed:
            result["passed"] = False
            result["notes"].append(
                f"Model {model} P95={p95:.0f}ms exceeds SLA of {max_p95}ms"
            )

    if result["passed"]:
        result["notes"].append("All models within SLA P95 threshold.")

    return result


def run_regression_baseline(case: dict, dry_run: bool) -> dict:
    """
    Run the full regression suite against Sonnet and check pass rate.

    The pass criterion is min_pass_rate (default 1.0 = all cases must pass).
    """
    model = case.get("model", MODEL_B)
    min_pass_rate = case["pass_criteria"]["min_pass_rate"]

    result = {
        "eval_id": case["id"],
        "description": case["description"],
        "pass_criteria": case["pass_criteria"],
        "model": model,
        "total_cases": 0,
        "passed_cases": 0,
        "actual_pass_rate": 0.0,
        "failed_cases": [],
        "passed": False,
        "notes": [],
    }

    if dry_run:
        reg_results = _mock_regression_results(model)
    else:
        from platform_eval.regression_suite import run_regression, REGRESSION_CASES
        reg_objs = run_regression(model)
        reg_results = [
            {
                "case_id": r.case_id,
                "passed": r.passed,
                "quality_score": r.quality_score,
                "failures": r.failures,
            }
            for r in reg_objs
        ]

    total = len(reg_results)
    passed = sum(1 for r in reg_results if r["passed"])
    failed_cases = [r["case_id"] for r in reg_results if not r["passed"]]
    actual_rate = passed / total if total > 0 else 0.0

    result["total_cases"] = total
    result["passed_cases"] = passed
    result["actual_pass_rate"] = round(actual_rate, 4)
    result["failed_cases"] = failed_cases
    result["passed"] = actual_rate >= min_pass_rate

    if result["passed"]:
        result["notes"].append(f"All {total} regression cases passed on {model}.")
    else:
        result["notes"].append(
            f"{len(failed_cases)} of {total} cases failed: {failed_cases}. "
            f"Pass rate {actual_rate:.1%} < required {min_pass_rate:.1%}"
        )

    return result


def run_ab_winner_determination(case: dict, dry_run: bool) -> dict:
    """
    Run an A/B experiment and verify a clear recommendation is produced.

    The pass criterion is that recommendation != "INCONCLUSIVE".
    """
    result = {
        "eval_id": case["id"],
        "description": case["description"],
        "pass_criteria": case["pass_criteria"],
        "experiment_id": None,
        "recommendation": None,
        "model_a_wins": None,
        "model_b_wins": None,
        "passed": False,
        "notes": [],
    }

    # Test prompts for the A/B experiment
    test_prompts = [
        "Explain the concept of recursion in programming in 2-3 sentences.",
        "What are three key differences between SQL and NoSQL databases?",
        "Write a Python function to check if a number is prime.",
        "Summarize the main causes of the French Revolution in bullet points.",
        "What is the difference between supervised and unsupervised machine learning?",
        "Explain REST API principles in simple terms.",
        "What is the time complexity of binary search and why?",
        "Describe the purpose of Docker containers in software development.",
        "What are the SOLID principles in object-oriented programming?",
        "Explain the difference between concurrency and parallelism.",
    ]

    if dry_run:
        exp_result = _mock_experiment_result()
    else:
        from ab_testing.experiment import run_experiment
        exp_obj = run_experiment(
            prompts=test_prompts,
            experiment_id="eval-ab-test",
        )
        exp_result = {
            "experiment_id": exp_obj.experiment_id,
            "prompts_tested": exp_obj.prompts_tested,
            "model_a_wins": exp_obj.model_a_wins,
            "model_b_wins": exp_obj.model_b_wins,
            "ties": exp_obj.ties,
            "recommendation": exp_obj.recommendation,
        }

    result["experiment_id"] = exp_result["experiment_id"]
    result["recommendation"] = exp_result["recommendation"]
    result["model_a_wins"] = exp_result["model_a_wins"]
    result["model_b_wins"] = exp_result["model_b_wins"]

    requires_recommendation = case["pass_criteria"].get("requires_recommendation", True)
    if requires_recommendation:
        result["passed"] = exp_result["recommendation"] != "INCONCLUSIVE"
        if result["passed"]:
            result["notes"].append(
                f"Clear recommendation produced: {exp_result['recommendation']} "
                f"(A={exp_result['model_a_wins']} wins, B={exp_result['model_b_wins']} wins)"
            )
        else:
            result["notes"].append(
                "No clear winner determined — result is INCONCLUSIVE. "
                "Consider running more samples or reviewing prompt diversity."
            )
    else:
        result["passed"] = True

    return result


# ─────────────────────────────────────────────────────────────────────────────
# Dispatch table
# ─────────────────────────────────────────────────────────────────────────────

_EVAL_RUNNERS = {
    "quality_threshold": run_quality_threshold,
    "cost_efficiency": run_cost_efficiency,
    "sla_compliance": run_sla_compliance,
    "regression_baseline": run_regression_baseline,
    "ab_winner_determination": run_ab_winner_determination,
}


# ─────────────────────────────────────────────────────────────────────────────
# Main runner
# ─────────────────────────────────────────────────────────────────────────────

def load_eval_cases(path: str = EVAL_CASES_PATH) -> list[dict]:
    """Load and return eval cases from JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def run_all_evals(
    cases: list[dict],
    dry_run: bool = False,
    filter_id: Optional[str] = None,
) -> list[dict]:
    """
    Run all (or a filtered subset of) eval cases.

    Args:
        cases: List of eval case dicts from eval_cases.json
        dry_run: If True, skip API calls and return mock results
        filter_id: If provided, only run the case with this ID

    Returns:
        List of result dicts, one per case run
    """
    if filter_id:
        cases = [c for c in cases if c["id"] == filter_id]
        if not cases:
            print(f"[EvalRunner] No eval case found with id='{filter_id}'")
            return []

    results = []
    total = len(cases)

    for i, case in enumerate(cases):
        case_id = case["id"]
        print(f"\n[EvalRunner] Running eval {i + 1}/{total}: {case_id}")
        if dry_run:
            print("  (DRY RUN — no API calls)")

        runner_fn = _EVAL_RUNNERS.get(case_id)
        if runner_fn is None:
            print(f"  [WARNING] No runner registered for eval id '{case_id}' — skipping.")
            results.append({
                "eval_id": case_id,
                "passed": None,
                "error": f"No runner registered for eval id '{case_id}'",
            })
            continue

        start = time.time()
        try:
            result = runner_fn(case, dry_run=dry_run)
        except Exception as e:
            import traceback
            print(f"  [ERROR] Eval '{case_id}' raised an exception: {e}")
            if VERBOSE:
                traceback.print_exc()
            result = {
                "eval_id": case_id,
                "passed": False,
                "error": str(e),
            }
        elapsed = time.time() - start

        result["elapsed_seconds"] = round(elapsed, 2)
        result["dry_run"] = dry_run
        results.append(result)

        status = "PASS" if result.get("passed") else "FAIL"
        notes = result.get("notes", [])
        notes_str = " | ".join(notes) if notes else ""
        print(f"  → {status} ({elapsed:.1f}s) {notes_str}")

    return results


def save_results(results: list[dict], path: str = EVAL_RESULTS_PATH) -> None:
    """Save eval results to JSON file."""
    output = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "total_cases": len(results),
        "passed": sum(1 for r in results if r.get("passed") is True),
        "failed": sum(1 for r in results if r.get("passed") is False),
        "skipped": sum(1 for r in results if r.get("passed") is None),
        "results": results,
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)
    print(f"\n[EvalRunner] Results saved to {path}")


def print_summary(results: list[dict]) -> None:
    """Print a final summary table."""
    sep = "=" * 60
    total = len(results)
    passed = sum(1 for r in results if r.get("passed") is True)
    failed = sum(1 for r in results if r.get("passed") is False)
    skipped = total - passed - failed

    print(f"\n{sep}")
    print("  EVAL RUNNER SUMMARY")
    print(sep)
    print(f"  Total:   {total}")
    print(f"  Passed:  {passed}")
    print(f"  Failed:  {failed}")
    print(f"  Skipped: {skipped}")
    print(sep)

    for r in results:
        status = "PASS" if r.get("passed") is True else "FAIL" if r.get("passed") is False else "SKIP"
        print(f"  [{status}] {r.get('eval_id', '?')}")

    overall = "ALL PASSED" if failed == 0 and skipped == 0 else "SOME FAILURES"
    print(f"\n  Overall: {overall}")
    print(f"{sep}\n")


# ─────────────────────────────────────────────────────────────────────────────
# CLI entry point
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Run evaluation cases for the AI product project.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python evals/eval_runner.py                          # Run all evals
  python evals/eval_runner.py --dry-run                # Mock run (no API)
  python evals/eval_runner.py --id quality_threshold   # Run one eval
  python evals/eval_runner.py --id cost_efficiency --dry-run
        """,
    )
    parser.add_argument(
        "--id",
        type=str,
        default=None,
        help="Run only the eval case with this ID",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Skip API calls and use mock data (for testing the runner itself)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=EVAL_RESULTS_PATH,
        help=f"Path to save results JSON (default: {EVAL_RESULTS_PATH})",
    )
    args = parser.parse_args()

    print(f"[EvalRunner] Loading eval cases from {EVAL_CASES_PATH}")
    cases = load_eval_cases()
    print(f"[EvalRunner] Loaded {len(cases)} eval cases")

    if args.dry_run:
        print("[EvalRunner] DRY RUN MODE — no API calls will be made")
        config.PROVIDER = "anthropic"  # default for dry-run (no real calls)
    else:
        _provider, _api_key = prov.choose_provider()
        config.PROVIDER = _provider
        if _provider == "anthropic":
            config.ANTHROPIC_API_KEY = _api_key
        else:
            config.OPENAI_API_KEY = _api_key

    results = run_all_evals(cases, dry_run=args.dry_run, filter_id=args.id)
    save_results(results, path=args.output)
    print_summary(results)

    # Exit with non-zero code if any evals failed
    if any(r.get("passed") is False for r in results):
        sys.exit(1)


if __name__ == "__main__":
    main()
