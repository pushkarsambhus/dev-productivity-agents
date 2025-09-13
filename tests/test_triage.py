from app.triage import triage_log

def test_detects_npm_404():
    res = triage_log("npm ERR! 404 Not Found")
    assert res["classification"] == "dependency_error"

def test_unknown_defaults():
    res = triage_log("No error here")
    assert "suggestions" in res
