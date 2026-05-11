"""
evals/eval_runner.py — Evaluate the agent against a test suite.

═══════════════════════════════════════════════════════════════════════════════
WHAT IS AN "EVAL"?

An eval is a structured way to measure whether your agent produces correct,
high-quality outputs across a set of representative inputs.

Unit tests (tests/) check MECHANICS — does the loop work, are IDs matched, etc.
Evals check QUALITY    — does the agent get the RIGHT answer, use the RIGHT tools?

THREE DIMENSIONS we measure here:
  1. Correctness   — does the answer contain expected keywords/numbers?
  2. Tool usage    — did the agent use the tools we expected it to?
  3. Efficiency    — how many turns did it take?

TRADE-OFFS:
  • String matching is fast and cheap but brittle (misses paraphrases).
  • LLM-as-judge is more flexible but costs extra API tokens.
  • Human review is most accurate but doesn't scale.

For learning: start with string matching (what's here), then add LLM-as-judge
once you understand the basics.

═══════════════════════════════════════════════════════════════════════════════

USAGE:
    cd 01-single-agent
    export ANTHROPIC_API_KEY="sk-ant-..."
    python evals/eval_runner.py                  # run all cases
    python evals/eval_runner.py --id math_basic  # run one case
    python evals/eval_runner.py --category math  # run a category
    python evals/eval_runner.py --verbose        # show full answers
"""

import json
import sys
import os
import time
import argparse
from dataclasses import dataclass, field
from typing import Optional

# Make sure the parent directory is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import config
from agent import run_agent


# ─────────────────────────────────────────────────────────────────────────────
# Data structures
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class EvalResult:
    case_id: str
    passed: bool
    score: float              # 0.0 – 1.0
    answer: str               # what the agent actually returned
    expected_fragments: list  # what we were looking for
    tools_expected: list
    tools_used: list          # not yet instrumented — placeholder
    latency_sec: float
    error: Optional[str] = None
    details: dict = field(default_factory=dict)


# ─────────────────────────────────────────────────────────────────────────────
# Evaluation logic
# ─────────────────────────────────────────────────────────────────────────────

def evaluate_answer(answer: str, case: dict) -> tuple[bool, float, list]:
    """
    Check whether the answer satisfies the eval case criteria.

    Returns:
        (passed, score, matched_fragments)

    Score breakdown:
      • 1.0  all expected fragments found
      • 0.5  at least half found
      • 0.0  none found
    """
    answer_lower = answer.lower()
    matched = []

    # Check 'expected_answer_contains' (ALL must be present)
    must_contain = case.get("expected_answer_contains", [])
    all_matched = True
    for fragment in must_contain:
        if fragment.lower() in answer_lower:
            matched.append(fragment)
        else:
            all_matched = False

    if must_contain:
        score = len(matched) / len(must_contain)
        return all_matched, score, matched

    # Check 'expected_answer_contains_any' (AT LEAST ONE must be present)
    any_contain = case.get("expected_answer_contains_any", [])
    if any_contain:
        for fragment in any_contain:
            if fragment.lower() in answer_lower:
                return True, 1.0, [fragment]
        return False, 0.0, []

    # No criteria defined → pass by default (useful for smoke tests)
    return True, 1.0, []


def run_single_case(case: dict, verbose: bool = False) -> EvalResult:
    """Run one eval case and return the result."""
    print(f"  Running: [{case['id']}] {case['description']}")

    # Temporarily override MAX_TURNS if the case specifies a limit
    original_max = config.MAX_TURNS
    if "max_turns" in case:
        config.MAX_TURNS = case["max_turns"]
    original_verbose = config.VERBOSE
    config.VERBOSE = verbose  # suppress internal logs unless verbose

    start = time.time()
    error = None
    answer = ""

    try:
        answer = run_agent(case["input"])
    except Exception as exc:
        error = str(exc)
        answer = ""
    finally:
        elapsed = time.time() - start
        config.MAX_TURNS = original_max
        config.VERBOSE = original_verbose

    # Evaluate the answer
    passed, score, matched = evaluate_answer(answer, case)

    # TODO: instrument tool tracking
    # Right now we can't easily know which tools were called without
    # adding a tracking hook to dispatch_tool(). For now we leave it empty.
    # Enhancement idea: wrap dispatch_tool with a context-local list collector.
    tools_used = []  # placeholder

    if verbose:
        print(f"    Answer: {answer[:300]}")
        print(f"    Score:  {score:.2f}  ({'PASS' if passed else 'FAIL'})")
        print(f"    Matched: {matched}")
        print(f"    Latency: {elapsed:.1f}s")

    return EvalResult(
        case_id=case["id"],
        passed=passed,
        score=score,
        answer=answer,
        expected_fragments=case.get("expected_answer_contains",
                                    case.get("expected_answer_contains_any", [])),
        tools_expected=case.get("expected_tools_used", []),
        tools_used=tools_used,
        latency_sec=elapsed,
        error=error,
    )


# ─────────────────────────────────────────────────────────────────────────────
# LLM-as-judge (optional, more powerful but uses extra tokens)
# ─────────────────────────────────────────────────────────────────────────────

def llm_judge(question: str, answer: str, expected_description: str) -> tuple[bool, str]:
    """
    Use Claude itself to judge whether an answer is correct.

    TRADE-OFF:
        + More flexible than string matching (handles paraphrases, equivalents)
        + Can explain WHY an answer is wrong
        - Costs extra API tokens (~$0.001 per eval case)
        - The judge model can also be wrong (though less often)
        - Adds latency

    TODO: uncomment and use this instead of evaluate_answer() for
          more sophisticated evaluations.
    """
    import anthropic as _anthropic

    judge_client = _anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
    prompt = f"""You are evaluating whether an AI assistant gave a correct answer.

QUESTION: {question}

EXPECTED: The answer should {expected_description}

ACTUAL ANSWER: {answer}

Reply with exactly "PASS" if the answer is correct, or "FAIL: <brief reason>" if not."""

    response = judge_client.messages.create(
        model="claude-haiku-4-5",   # use cheapest model for judging
        max_tokens=100,
        messages=[{"role": "user", "content": prompt}],
    )
    verdict = response.content[0].text.strip()
    passed = verdict.startswith("PASS")
    return passed, verdict


# ─────────────────────────────────────────────────────────────────────────────
# Report generation
# ─────────────────────────────────────────────────────────────────────────────

def print_report(results: list[EvalResult]) -> None:
    total = len(results)
    passed = sum(1 for r in results if r.passed)
    avg_score = sum(r.score for r in results) / total if total else 0
    avg_latency = sum(r.latency_sec for r in results) / total if total else 0

    print(f"\n{'═'*60}")
    print(f"EVAL REPORT  — {passed}/{total} passed  ({avg_score*100:.0f}% avg score)")
    print(f"{'═'*60}")
    print(f"{'ID':<25} {'Status':<8} {'Score':>6}  {'Latency':>8}")
    print(f"{'─'*60}")
    for r in results:
        status = "✓ PASS" if r.passed else "✗ FAIL"
        latency = f"{r.latency_sec:.1f}s"
        print(f"{r.case_id:<25} {status:<8} {r.score:>6.2f}  {latency:>8}")
        if r.error:
            print(f"  ERROR: {r.error}")
    print(f"{'─'*60}")
    print(f"Average latency: {avg_latency:.1f}s")
    print(f"{'═'*60}\n")

    # Save results to JSON for further analysis
    out_path = os.path.join(os.path.dirname(__file__), "eval_results.json")
    with open(out_path, "w") as f:
        json.dump(
            [
                {
                    "id": r.case_id,
                    "passed": r.passed,
                    "score": r.score,
                    "latency_sec": r.latency_sec,
                    "answer_preview": r.answer[:200],
                    "error": r.error,
                }
                for r in results
            ],
            f,
            indent=2,
        )
    print(f"Results saved to: {out_path}")


# ─────────────────────────────────────────────────────────────────────────────
# Main CLI
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Run agent evals")
    parser.add_argument("--id", help="Run a single eval case by ID")
    parser.add_argument("--category", help="Run all cases in a category")
    parser.add_argument("--verbose", action="store_true", help="Show full answers")
    args = parser.parse_args()

    if not config.ANTHROPIC_API_KEY:
        print("ERROR: ANTHROPIC_API_KEY is not set. Evals require a real API key.")
        print("Set it with: export ANTHROPIC_API_KEY='sk-ant-...'")
        sys.exit(1)

    cases_path = os.path.join(os.path.dirname(__file__), "eval_cases.json")
    with open(cases_path) as f:
        all_cases = json.load(f)

    # Filter cases
    if args.id:
        cases = [c for c in all_cases if c["id"] == args.id]
    elif args.category:
        cases = [c for c in all_cases if c.get("category") == args.category]
    else:
        cases = all_cases

    if not cases:
        print(f"No eval cases found for filter: id={args.id}, category={args.category}")
        sys.exit(1)

    print(f"\nRunning {len(cases)} eval case(s)...\n")
    results = []
    for case in cases:
        result = run_single_case(case, verbose=args.verbose)
        results.append(result)

    print_report(results)

    # Exit with non-zero code if any tests failed (useful in CI)
    failed = sum(1 for r in results if not r.passed)
    sys.exit(failed)


if __name__ == "__main__":
    main()
