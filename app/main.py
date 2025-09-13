from fastapi import FastAPI
from pydantic import BaseModel
from .triage import triage_log
from .tests_agent import suggest_tests

app = FastAPI(title="Dev Productivity Agents", version="0.1.0")

class LogPayload(BaseModel):
    log: str | None = None

class LogFilePayload(BaseModel):
    path: str | None = None

class TestSuggestPayload(BaseModel):
    repo: str
    diff: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/triage")
def triage(payload: LogPayload | LogFilePayload):
    text = ""
    if isinstance(payload, LogPayload) and payload.log:
        text = payload.log
    elif isinstance(payload, LogFilePayload) and payload.path:
        with open(payload.path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
    else:
        return {"error": "Provide 'log' string or 'path' to a log file."}

    result = triage_log(text)
    return result

@app.post("/suggest-tests")
def suggest_tests_api(payload: TestSuggestPayload):
    return {"tool": "qa_agent", **suggest_tests(payload.repo, payload.diff)}
