import json
import os
import uuid
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import claude_service
import pdf_parser

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

ADMIN_PIN = os.getenv("ADMIN_PIN", "1234")
STUDENT_PIN = os.getenv("STUDENT_PIN", "5678")
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)
SESSIONS_FILE = DATA_DIR / "sessions.json"
PROGRESS_FILE = DATA_DIR / "progress.json"
SETTINGS_FILE = DATA_DIR / "settings.json"

app = FastAPI(title="RSM Math Tutor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow LAN devices to reach student API
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Admin-only route prefixes — blocked from non-localhost devices
ADMIN_ROUTES = ["/api/auth/admin", "/api/upload", "/api/sessions", "/api/settings", "/api/extract-from-image"]

@app.middleware("http")
async def restrict_admin_to_localhost(request, call_next):
    client_host = request.client.host if request.client else ""
    is_local = client_host in ("127.0.0.1", "::1", "localhost")
    is_admin_route = any(request.url.path.startswith(p) for p in ADMIN_ROUTES)
    if is_admin_route and not is_local:
        from fastapi.responses import JSONResponse
        return JSONResponse({"detail": "Admin access is only available on the host computer."}, status_code=403)
    return await call_next(request)


# ---------- helpers ----------

def load_sessions() -> dict:
    if SESSIONS_FILE.exists():
        return json.loads(SESSIONS_FILE.read_text())
    return {}


def save_sessions(data: dict):
    SESSIONS_FILE.write_text(json.dumps(data, indent=2))


def load_progress() -> dict:
    if PROGRESS_FILE.exists():
        return json.loads(PROGRESS_FILE.read_text())
    return {}


def save_progress(data: dict):
    PROGRESS_FILE.write_text(json.dumps(data, indent=2))


def load_settings() -> dict:
    if SETTINGS_FILE.exists():
        return json.loads(SETTINGS_FILE.read_text())
    # defaults: prefer env vars
    return {
        "provider": "anthropic",
        "anthropic_key": os.getenv("ANTHROPIC_API_KEY", ""),
        "openai_key": os.getenv("OPENAI_API_KEY", ""),
    }


def save_settings(data: dict):
    SETTINGS_FILE.write_text(json.dumps(data, indent=2))


def get_llm_args() -> tuple[str, str]:
    """Return (provider, api_key) from saved settings."""
    s = load_settings()
    provider = s.get("provider", "anthropic")
    if provider == "openai":
        return provider, s.get("openai_key", "")
    if provider == "claude-cli":
        return provider, ""
    return "anthropic", s.get("anthropic_key", "")


def get_active_session() -> Optional[dict]:
    sessions = load_sessions()
    for s in sessions.values():
        if s.get("active"):
            return s
    return None


# ---------- auth ----------

class PinRequest(BaseModel):
    pin: str


@app.post("/api/auth/admin")
def auth_admin(req: PinRequest):
    if req.pin != ADMIN_PIN:
        raise HTTPException(status_code=401, detail="Invalid admin PIN")
    return {"role": "admin"}


@app.post("/api/auth/student")
def auth_student(req: PinRequest):
    if req.pin != STUDENT_PIN:
        raise HTTPException(status_code=401, detail="Invalid student PIN")
    return {"role": "student"}


# ---------- AI provider settings ----------

class ProviderSettings(BaseModel):
    provider: str          # "anthropic" | "openai" | "claude-cli"
    anthropic_key: Optional[str] = ""
    openai_key: Optional[str] = ""


@app.get("/api/settings")
def get_settings():
    s = load_settings()
    # Mask keys for display
    def mask(k: str) -> str:
        if len(k) > 8:
            return k[:4] + "••••" + k[-4:]
        return "••••" if k else ""
    return {
        "provider": s.get("provider", "anthropic"),
        "anthropic_key_set": bool(s.get("anthropic_key")),
        "openai_key_set": bool(s.get("openai_key")),
        "anthropic_key_preview": mask(s.get("anthropic_key", "")),
        "openai_key_preview": mask(s.get("openai_key", "")),
    }


@app.post("/api/settings")
def update_settings(body: ProviderSettings):
    if body.provider not in ("anthropic", "openai", "claude-cli"):
        raise HTTPException(400, "provider must be 'anthropic', 'openai', or 'claude-cli'")
    s = load_settings()
    s["provider"] = body.provider
    if body.anthropic_key:
        s["anthropic_key"] = body.anthropic_key
    if body.openai_key:
        s["openai_key"] = body.openai_key
    save_settings(s)
    return {"ok": True, "provider": s["provider"]}


# ---------- sessions ----------

@app.get("/api/sessions")
def list_sessions():
    return list(load_sessions().values())


@app.get("/api/sessions/active")
def get_active():
    session = get_active_session()
    if not session:
        return None
    return session


@app.delete("/api/sessions/{session_id}")
def delete_session(session_id: str):
    sessions = load_sessions()
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    del sessions[session_id]
    save_sessions(sessions)
    # Also clean up progress for this session
    progress = load_progress()
    if session_id in progress:
        del progress[session_id]
        save_progress(progress)
    return {"ok": True}


@app.post("/api/sessions/{session_id}/activate")
def activate_session(session_id: str):
    sessions = load_sessions()
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    for sid in sessions:
        sessions[sid]["active"] = sid == session_id
    save_sessions(sessions)
    return sessions[session_id]


# ---------- image OCR ----------

class ImageOCRRequest(BaseModel):
    image_b64: str        # base64-encoded image
    media_type: str = "image/png"   # image/png or image/jpeg


@app.post("/api/extract-from-image")
def extract_from_image(req: ImageOCRRequest):
    provider, api_key = get_llm_args()
    try:
        text = claude_service.extract_text_from_image(
            req.image_b64, req.media_type, provider, api_key
        )
        return {"text": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------- PDF upload ----------

@app.post("/api/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")

    file_bytes = await file.read()
    pdf_text = pdf_parser.extract_text_from_pdf(file_bytes)

    if not pdf_text.strip():
        raise HTTPException(
            status_code=422,
            detail="Could not extract text from PDF. It may be a scanned image.",
        )

    provider, api_key = get_llm_args()
    try:
        raw_questions = claude_service.extract_questions_from_text(pdf_text, provider, api_key)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    session_id = str(uuid.uuid4())[:8]
    questions = []
    for i, q in enumerate(raw_questions):
        questions.append(
            {
                "id": f"q{i+1}",
                "number": q.get("number", str(i + 1)),
                "text": q.get("text", ""),
                "hint1": None,
                "hint2": None,
                "hint3": None,
                "solution": None,
                "hints_generated": False,
                "hints_released": 0,
                "active": True,
            }
        )

    session = {
        "id": session_id,
        "filename": file.filename,
        "questions": questions,
        "active": False,
    }

    sessions = load_sessions()
    sessions[session_id] = session
    save_sessions(sessions)

    return session


# ---------- questions ----------

@app.get("/api/sessions/{session_id}/questions")
def get_questions(session_id: str):
    sessions = load_sessions()
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return sessions[session_id]["questions"]


class QuestionUpdate(BaseModel):
    text: Optional[str] = None
    active: Optional[bool] = None
    hints_released: Optional[int] = None


@app.patch("/api/sessions/{session_id}/questions/{question_id}")
def update_question(session_id: str, question_id: str, update: QuestionUpdate):
    sessions = load_sessions()
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    questions = sessions[session_id]["questions"]
    q = next((x for x in questions if x["id"] == question_id), None)
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")

    if update.text is not None:
        q["text"] = update.text
    if update.active is not None:
        q["active"] = update.active
    if update.hints_released is not None:
        q["hints_released"] = update.hints_released

    save_sessions(sessions)
    return q


@app.post("/api/sessions/{session_id}/questions/{question_id}/generate-similar")
def generate_similar(session_id: str, question_id: str):
    sessions = load_sessions()
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    questions = sessions[session_id]["questions"]
    source_q = next((x for x in questions if x["id"] == question_id), None)
    if not source_q:
        raise HTTPException(status_code=404, detail="Question not found")

    provider, api_key = get_llm_args()
    try:
        result = claude_service.generate_similar_question(source_q["text"], provider, api_key)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Build new question id — count existing practice cards for this source
    practice_count = sum(
        1 for q in questions if q.get("source_id") == question_id
    )
    new_id = f"{question_id}_p{practice_count + 1}"
    new_q = {
        "id": new_id,
        "number": f"{source_q['number']} (Practice {practice_count + 1})",
        "text": result["text"],
        "hint1": None, "hint2": None, "hint3": None, "solution": None,
        "hints_generated": False,
        "hints_released": 0,
        "active": True,
        "source_id": question_id,   # marks this as a generated practice card
        "is_practice": True,
    }

    # Insert immediately after the source question (and its existing practice cards)
    insert_idx = len(questions)
    for i, q in enumerate(questions):
        if q["id"] == question_id or q.get("source_id") == question_id:
            insert_idx = i + 1
    questions.insert(insert_idx, new_q)

    save_sessions(sessions)
    return new_q


@app.post("/api/sessions/{session_id}/questions/{question_id}/generate-hints")
def generate_hints(session_id: str, question_id: str):
    sessions = load_sessions()
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    questions = sessions[session_id]["questions"]
    q = next((x for x in questions if x["id"] == question_id), None)
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")

    provider, api_key = get_llm_args()
    result = claude_service.generate_hints_and_solution(q["text"], provider, api_key)
    q["hint1"] = result["hint1"]
    q["hint2"] = result["hint2"]
    q["hint3"] = result["hint3"]
    q["solution"] = result["solution"]
    q["hints_generated"] = True

    save_sessions(sessions)
    return q


# ---------- student view ----------

@app.get("/api/student/questions")
def student_questions():
    session = get_active_session()
    if not session:
        return []

    progress = load_progress()
    session_id = session["id"]
    session_progress = progress.get(session_id, {})

    result = []
    for q in session["questions"]:
        if not q.get("active"):
            continue
        qp = session_progress.get(q["id"], {})
        hints_seen = qp.get("hints_seen", 0)
        max_hints = min(q.get("hints_released", 0), 3)
        visible_hints = []
        for i in range(1, min(hints_seen, max_hints) + 1):
            hint_text = q.get(f"hint{i}")
            if hint_text:
                visible_hints.append({"level": i, "text": hint_text})

        result.append(
            {
                "id": q["id"],
                "number": q["number"],
                "text": q["text"],
                "hints_available": max_hints,
                "hints_seen": hints_seen,
                "visible_hints": visible_hints,
                "completed": qp.get("completed", False),
                "session_id": session_id,
            }
        )
    return result


class HintRequest(BaseModel):
    session_id: str
    question_id: str


@app.post("/api/student/request-hint")
def request_hint(req: HintRequest):
    sessions = load_sessions()
    if req.session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    questions = sessions[req.session_id]["questions"]
    q = next((x for x in questions if x["id"] == req.question_id), None)
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")

    progress = load_progress()
    session_progress = progress.setdefault(req.session_id, {})
    qp = session_progress.setdefault(req.question_id, {"hints_seen": 0, "completed": False})

    max_available = min(q.get("hints_released", 0), 3)
    if qp["hints_seen"] >= max_available:
        return {"message": "no_more_hints", "hints_seen": qp["hints_seen"]}

    qp["hints_seen"] += 1
    save_progress(progress)

    hint_text = q.get(f"hint{qp['hints_seen']}")
    return {
        "level": qp["hints_seen"],
        "text": hint_text,
        "hints_seen": qp["hints_seen"],
        "max_available": max_available,
    }


class AnswerSubmission(BaseModel):
    session_id: str
    question_id: str
    answer: str


@app.post("/api/student/submit-answer")
def submit_answer(submission: AnswerSubmission):
    sessions = load_sessions()
    if submission.session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    questions = sessions[submission.session_id]["questions"]
    q = next((x for x in questions if x["id"] == submission.question_id), None)
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")

    provider, api_key = get_llm_args()
    result = claude_service.check_student_answer(
        q["text"], submission.answer, provider, api_key,
        known_solution=q.get("solution") or "",
    )

    if result.get("correct"):
        progress = load_progress()
        session_progress = progress.setdefault(submission.session_id, {})
        qp = session_progress.setdefault(submission.question_id, {"hints_seen": 0, "completed": False})
        qp["completed"] = True
        save_progress(progress)

    return result


# ---------- progress ----------

@app.get("/api/progress/{session_id}")
def get_progress(session_id: str):
    sessions = load_sessions()
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    progress = load_progress()
    session_progress = progress.get(session_id, {})
    questions = sessions[session_id]["questions"]
    active_questions = [q for q in questions if q.get("active")]

    total = len(active_questions)
    completed = sum(
        1 for q in active_questions if session_progress.get(q["id"], {}).get("completed")
    )

    return {
        "total": total,
        "completed": completed,
        "percent": round(completed / total * 100) if total else 0,
        "by_question": {
            q["id"]: session_progress.get(q["id"], {"hints_seen": 0, "completed": False})
            for q in active_questions
        },
    }
