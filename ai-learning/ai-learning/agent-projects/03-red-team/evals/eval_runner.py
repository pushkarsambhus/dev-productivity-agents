"""
evals/eval_runner.py — Structured evaluation of red team defences.

USAGE:
    cd 03-red-team
    export ANTHROPIC_API_KEY="sk-ant-..."
    python evals/eval_runner.py           # all eval cases
    python evals/eval_runner.py --id hardened_bypass_rate
    python evals/eval_runner.py --verbose

This runner answers the PM/EM question:
  "Is this system safe enough to ship?"
By measuring bypass rates against configurable thresholds.
"""

import sys, os, json, argparse, time
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import config
from red_team_runner import run_assessment, AssessmentReport


def evaluate_case(case: dict, verbose: bool = False) -> dict:
    print(f"  Running: [{case['id']}] {case['description']}")
    start = time.time()

    report: AssessmentReport = run_assessment(
        suite=case.get("suite", "all"),
        hardened=case.get("hardened", False),
    )
    elapsed = time.time() - start

    criteria = case.get("pass_criteria", {})
    failures = []

    if "max_bypass_rate" in criteria:
        if report.bypass_rate > criteria["max_bypass_rate"]:
            failures.append(
                f"bypass_rate {report.bypass_rate:.0%} > threshold {criteria['max_bypass_rate']:.0%}"
            )

    if "min_defence_rate" in criteria:
        defence_rate = report.defended / report.total if report.total else 0
        if defence_rate < criteria["min_defence_rate"]:
            failures.append(
                f"defence_rate {defence_rate:.0%} < threshold {criteria['min_defence_rate']:.0%}"
            )

    if "max_critical_count" in criteria:
        count = report.by_severity.get(config.SEVERITY_CRITICAL, 0)
        if count > criteria["max_critical_count"]:
            failures.append(f"critical_count {count} > {criteria['max_critical_count']}")

    if "max_high_count" in criteria:
        count = report.by_severity.get(config.SEVERITY_HIGH, 0)
        if count > criteria["max_high_count"]:
            failures.append(f"high_count {count} > {criteria['max_high_count']}")

    passed = len(failures) == 0
    status = "✓ PASS" if passed else "✗ FAIL"
    print(f"    {status}  bypass={report.bypass_rate:.0%}  defended={report.defended}/{report.total}  ({elapsed:.0f}s)")
    if failures:
        for f in failures:
            print(f"    ✗ {f}")

    return {
        "id": case["id"],
        "passed": passed,
        "bypass_rate": report.bypass_rate,
        "bypassed": report.bypassed,
        "defended": report.defended,
        "total": report.total,
        "failures": failures,
        "latency_sec": elapsed,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", help="Run single eval case")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    if not config.ANTHROPIC_API_KEY:
        print("ERROR: ANTHROPIC_API_KEY not set.")
        sys.exit(1)

    cases_path = os.path.join(os.path.dirname(__file__), "eval_cases.json")
    with open(cases_path) as f:
        cases = json.load(f)

    if args.id:
        cases = [c for c in cases if c["id"] == args.id]

    print(f"\nRunning {len(cases)} red-team eval case(s)...\n")
    results = [evaluate_case(c, verbose=args.verbose) for c in cases]

    total = len(results)
    passed = sum(1 for r in results if r["passed"])
    print(f"\n{'═'*55}")
    print(f"RED TEAM EVALS: {passed}/{total} passed")
    print(f"{'═'*55}\n")

    out = os.path.join(os.path.dirname(__file__), "eval_results.json")
    with open(out, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Results saved to: {out}")

    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
