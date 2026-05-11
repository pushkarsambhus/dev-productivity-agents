"""
evals/eval_runner.py — Evaluate the multi-agent pipeline.

LEARNING NOTE — What's different from the single-agent eval?
    In multi-agent systems we evaluate at two levels:

    1. PIPELINE level  — does the final output meet quality standards?
       (same as single-agent eval)

    2. PROCESS level   — did the pipeline run correctly?
       - Did all expected agents run?
       - Were revision rounds triggered appropriately?
       - Did the Critic's feedback actually improve the draft?

    Process-level evals catch bugs like:
       - Writer ignoring Critic feedback
       - Researcher not being called at all
       - Pipeline stopping too early

USAGE:
    cd 02-multi-agent
    export ANTHROPIC_API_KEY="sk-ant-..."
    python evals/eval_runner.py
    python evals/eval_runner.py --id factual_accuracy
    python evals/eval_runner.py --category pipeline
    python evals/eval_runner.py --verbose
"""

import json
import sys
import os
import time
import argparse
from dataclasses import dataclass, field
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import config
from orchestrator import run_pipeline, run_parallel_research, PipelineState


# ─────────────────────────────────────────────────────────────────────────────
# Data structures
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class MultiAgentEvalResult:
    case_id: str
    passed: bool
    score: float               # 0.0 – 1.0
    final_output: str
    pipeline_steps: list       # which agents ran
    revision_count: int
    latency_sec: float
    checks_passed: list
    checks_failed: list
    error: Optional[str] = None


# ─────────────────────────────────────────────────────────────────────────────
# Check implementations
# ─────────────────────────────────────────────────────────────────────────────

def run_checks(state: PipelineState, checks: dict) -> tuple[list, list]:
    """
    Run all configured checks against a PipelineState.

    Returns (passed_checks, failed_checks)
    """
    passed = []
    failed = []
    output = state.final_output
    output_lower = output.lower()
    words = output.split()

    # ── Content checks ────────────────────────────────────────────────────────
    if "output_contains_any" in checks:
        fragments = checks["output_contains_any"]
        if any(f.lower() in output_lower for f in fragments):
            passed.append(f"output_contains_any: found one of {fragments}")
        else:
            failed.append(f"output_contains_any: none of {fragments} found in output")

    if "output_contains_all" in checks:
        fragments = checks["output_contains_all"]
        missing = [f for f in fragments if f.lower() not in output_lower]
        if not missing:
            passed.append(f"output_contains_all: all {len(fragments)} fragments found")
        else:
            failed.append(f"output_contains_all: missing {missing}")

    # ── Length checks ─────────────────────────────────────────────────────────
    if "output_min_words" in checks:
        minimum = checks["output_min_words"]
        if len(words) >= minimum:
            passed.append(f"output_min_words: {len(words)} >= {minimum}")
        else:
            failed.append(f"output_min_words: {len(words)} < {minimum}")

    if "output_max_words" in checks:
        maximum = checks["output_max_words"]
        if len(words) <= maximum:
            passed.append(f"output_max_words: {len(words)} <= {maximum}")
        else:
            failed.append(f"output_max_words: {len(words)} > {maximum}")

    # ── Pipeline process checks ───────────────────────────────────────────────
    if "pipeline_steps_include" in checks:
        agents_ran = {step["agent"] for step in state.steps}
        required = set(checks["pipeline_steps_include"])
        missing_agents = required - agents_ran
        if not missing_agents:
            passed.append(f"pipeline_steps_include: all required agents ran {required}")
        else:
            failed.append(f"pipeline_steps_include: agents {missing_agents} did not run")

    if "min_steps" in checks:
        minimum = checks["min_steps"]
        if len(state.steps) >= minimum:
            passed.append(f"min_steps: {len(state.steps)} >= {minimum}")
        else:
            failed.append(f"min_steps: {len(state.steps)} < {minimum}")

    return passed, failed


def run_parallel_checks(results: list[str], checks: dict) -> tuple[list, list]:
    """Check results from run_parallel_research."""
    passed = []
    failed = []

    if checks.get("all_results_non_empty"):
        if all(r and len(r) > 10 for r in results):
            passed.append("all_results_non_empty: ✓")
        else:
            failed.append("all_results_non_empty: some results are empty")

    if "result_count" in checks:
        expected = checks["result_count"]
        if len(results) == expected:
            passed.append(f"result_count: {len(results)} == {expected}")
        else:
            failed.append(f"result_count: got {len(results)}, expected {expected}")

    return passed, failed


# ─────────────────────────────────────────────────────────────────────────────
# Case runner
# ─────────────────────────────────────────────────────────────────────────────

def run_single_case(case: dict, verbose: bool = False) -> MultiAgentEvalResult:
    """Execute one eval case and collect metrics."""
    print(f"  Running: [{case['id']}] {case['description']}")

    original_verbose = config.VERBOSE
    config.VERBOSE = verbose

    start = time.time()
    error = None
    state = None
    checks_passed = []
    checks_failed = []

    try:
        eval_type = case.get("eval_type", "pipeline")
        checks = case.get("checks", {})

        if eval_type == "parallel_research":
            # Special case: test run_parallel_research
            topics = case["request"]
            results = run_parallel_research(topics)
            checks_passed, checks_failed = run_parallel_checks(results, checks)
            # Create a fake state for the result object
            from orchestrator import PipelineState
            state = PipelineState(user_request=str(topics))
            state.final_output = "\n\n".join(results)
        else:
            state = run_pipeline(case["request"])
            checks_passed, checks_failed = run_checks(state, checks)

    except Exception as exc:
        error = str(exc)
        from orchestrator import PipelineState
        state = state or PipelineState(user_request=case.get("request", ""))
    finally:
        elapsed = time.time() - start
        config.VERBOSE = original_verbose

    passed = len(checks_failed) == 0 and error is None
    score = len(checks_passed) / max(len(checks_passed) + len(checks_failed), 1)

    if verbose:
        print(f"    Output:    {state.final_output[:200]}")
        print(f"    Passed:    {checks_passed}")
        print(f"    Failed:    {checks_failed}")
        print(f"    Revisions: {state.revision_count}")
        print(f"    Latency:   {elapsed:.1f}s")

    return MultiAgentEvalResult(
        case_id=case["id"],
        passed=passed,
        score=score,
        final_output=state.final_output,
        pipeline_steps=[s["agent"] for s in state.steps],
        revision_count=state.revision_count,
        latency_sec=elapsed,
        checks_passed=checks_passed,
        checks_failed=checks_failed,
        error=error,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Report
# ─────────────────────────────────────────────────────────────────────────────

def print_report(results: list[MultiAgentEvalResult]) -> None:
    total = len(results)
    passed = sum(1 for r in results if r.passed)
    avg_score = sum(r.score for r in results) / total if total else 0
    avg_latency = sum(r.latency_sec for r in results) / total if total else 0
    avg_revisions = sum(r.revision_count for r in results) / total if total else 0

    print(f"\n{'═'*70}")
    print(f"MULTI-AGENT EVAL REPORT  — {passed}/{total} passed  ({avg_score*100:.0f}% avg score)")
    print(f"{'═'*70}")
    print(f"{'ID':<25} {'Status':<10} {'Score':>6}  {'Rev':>4}  {'Latency':>8}")
    print(f"{'─'*70}")
    for r in results:
        status = "✓ PASS" if r.passed else "✗ FAIL"
        latency = f"{r.latency_sec:.1f}s"
        rev = str(r.revision_count)
        print(f"{r.case_id:<25} {status:<10} {r.score:>6.2f}  {rev:>4}  {latency:>8}")
        if r.checks_failed:
            for f in r.checks_failed:
                print(f"    ✗ {f}")
        if r.error:
            print(f"    ERROR: {r.error}")
    print(f"{'─'*70}")
    print(f"Avg latency: {avg_latency:.1f}s  |  Avg revisions: {avg_revisions:.1f}")
    print(f"{'═'*70}\n")

    out_path = os.path.join(os.path.dirname(__file__), "eval_results.json")
    with open(out_path, "w") as f:
        json.dump(
            [
                {
                    "id": r.case_id,
                    "passed": r.passed,
                    "score": r.score,
                    "revision_count": r.revision_count,
                    "latency_sec": r.latency_sec,
                    "pipeline_steps": r.pipeline_steps,
                    "checks_failed": r.checks_failed,
                    "error": r.error,
                }
                for r in results
            ],
            f,
            indent=2,
        )
    print(f"Results saved to: {out_path}")


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Multi-agent eval runner")
    parser.add_argument("--id", help="Run a single eval by ID")
    parser.add_argument("--category", help="Run a category of evals")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    if not config.ANTHROPIC_API_KEY:
        print("ERROR: ANTHROPIC_API_KEY is not set.")
        sys.exit(1)

    cases_path = os.path.join(os.path.dirname(__file__), "eval_cases.json")
    with open(cases_path) as f:
        all_cases = json.load(f)

    if args.id:
        cases = [c for c in all_cases if c["id"] == args.id]
    elif args.category:
        cases = [c for c in all_cases if c.get("category") == args.category]
    else:
        cases = all_cases

    if not cases:
        print("No cases matched the filter.")
        sys.exit(1)

    print(f"\nRunning {len(cases)} multi-agent eval case(s)...\n")
    results = [run_single_case(c, verbose=args.verbose) for c in cases]
    print_report(results)

    failed = sum(1 for r in results if not r.passed)
    sys.exit(failed)


if __name__ == "__main__":
    main()
