def suggest_tests(repo: str, diff: str) -> dict:
    ideas = []
    if "endpoint" in diff:
        ideas.append("Add API contract tests for new endpoint")
    if "schema" in diff or "db" in diff:
        ideas.append("Add DB migration tests")
    if not ideas:
        ideas = ["Add unit tests", "Add integration test", "Add negative test"]
    return {"repo": repo, "diff_summary": diff[:200], "suggested_tests": ideas}
