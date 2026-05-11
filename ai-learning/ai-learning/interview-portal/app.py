import asyncio
import importlib.util
import json
import sqlite3
import uuid
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Optional

import anthropic
import openai as openai_lib
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# ── Setup ─────────────────────────────────────────────────────────────────────

BASE_DIR             = Path(__file__).parent
DB_PATH              = BASE_DIR / "sessions.db"
CUSTOM_Q_DIR         = BASE_DIR / "custom_questions"
CUSTOM_Q_DIR.mkdir(exist_ok=True)

app = FastAPI(title="Interview Prep Portal")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Client is built per-request based on provider + api_key supplied by the user.

# ── Database ──────────────────────────────────────────────────────────────────

@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    with get_db() as db:
        db.executescript("""
            CREATE TABLE IF NOT EXISTS sessions (
                id          TEXT PRIMARY KEY,
                position    TEXT NOT NULL,
                questions   TEXT NOT NULL,
                created_at  TEXT NOT NULL,
                provider    TEXT NOT NULL DEFAULT 'anthropic',
                api_key     TEXT NOT NULL DEFAULT ''
            );
            CREATE TABLE IF NOT EXISTS answers (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id      TEXT NOT NULL,
                question_index  INTEGER NOT NULL,
                user_answer     TEXT NOT NULL,
                is_correct      INTEGER NOT NULL,
                feedback        TEXT,
                submitted_at    TEXT NOT NULL,
                FOREIGN KEY (session_id) REFERENCES sessions(id)
            );
            CREATE TABLE IF NOT EXISTS deferred (
                session_id      TEXT NOT NULL,
                question_index  INTEGER NOT NULL,
                PRIMARY KEY (session_id, question_index),
                FOREIGN KEY (session_id) REFERENCES sessions(id)
            );
        """)

init_db()

# ── Models ────────────────────────────────────────────────────────────────────

class CreateSessionRequest(BaseModel):
    position: str
    num_questions: int = 10
    custom_topics: Optional[str] = None
    question_packs: list[str] = []   # pack IDs (file stems) to include
    provider: str = "anthropic"      # "anthropic" | "openai"
    api_key: str = ""                # key supplied by the user in the UI

class SubmitAnswerRequest(BaseModel):
    question_index: int
    user_answer: str

class DeferRequest(BaseModel):
    question_index: int

# ── Custom question packs ─────────────────────────────────────────────────────

_REQUIRED = {"type", "difficulty", "topic", "question", "correct_answer", "explanation", "remember"}
_VALID_TYPES = {"mcq", "find_the_bug", "coding"}
_VALID_DIFFS = {"easy", "medium", "hard"}

def _validate_q(q: dict) -> Optional[str]:
    missing = _REQUIRED - set(q)
    if missing:
        return f"missing fields: {sorted(missing)}"
    if q["type"] not in _VALID_TYPES:
        return f"invalid type '{q['type']}'"
    if q["difficulty"] not in _VALID_DIFFS:
        return f"invalid difficulty '{q['difficulty']}'"
    if q["type"] == "mcq" and "options" not in q:
        return "mcq requires 'options'"
    return None


def load_packs() -> dict:
    """Import every non-underscore .py in custom_questions/ and extract QUESTIONS + CONCEPTS."""
    packs = {}
    for py_file in sorted(CUSTOM_Q_DIR.glob("*.py")):
        if py_file.name.startswith("_"):
            continue
        try:
            spec = importlib.util.spec_from_file_location(py_file.stem, py_file)
            mod  = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)

            if not hasattr(mod, "QUESTIONS") or not isinstance(mod.QUESTIONS, list):
                continue

            questions, errors = [], []
            for i, raw in enumerate(mod.QUESTIONS):
                err = _validate_q(raw)
                if err:
                    errors.append(f"Q{i+1}: {err}")
                else:
                    q = dict(raw)
                    q["source"] = py_file.stem   # track origin
                    questions.append(q)

            packs[py_file.stem] = {
                "id":          py_file.stem,
                "name":        getattr(mod, "NAME",        py_file.stem.replace("_", " ").title()),
                "description": getattr(mod, "DESCRIPTION", ""),
                "icon":        getattr(mod, "ICON",        "📝"),
                "concepts":    getattr(mod, "CONCEPTS",    []),   # concept walkthroughs
                "questions":   questions,
                "count":       len(questions),
                "errors":      errors,
            }
        except Exception as exc:
            packs[py_file.stem] = {
                "id": py_file.stem, "name": py_file.stem,
                "load_error": str(exc), "count": 0, "questions": [], "errors": [], "concepts": [],
            }
    return packs


@app.get("/api/question-packs")
async def list_question_packs():
    packs = load_packs()
    return [
        {
            "id":          p["id"],
            "name":        p["name"],
            "description": p.get("description", ""),
            "icon":        p.get("icon", "📝"),
            "count":       p["count"],
            "errors":      p.get("errors", []),
            "load_error":  p.get("load_error"),
        }
        for p in packs.values()
    ]


# ── Question generation ───────────────────────────────────────────────────────

POSITION_LANGUAGE = {
    # Your target roles
    "ai / ml":          "Python",
    "ai/ml":            "Python",
    "ai platform":      "Python",
    "evaluation":       "Python",
    "red team":         "Python",
    "product manager":  "No code — use pseudocode/SQL/Python snippets for analytical questions",
    "automation test":  "Python",
    "engineering manager": "Python (for system-design/technical questions)",
    "technical program": "Python (for estimation/system-design questions)",
    "tpm":              "Python (for estimation/system-design questions)",
    # General roles
    "frontend":         "JavaScript/TypeScript",
    "backend":          "Python",
    "full stack":       "JavaScript/Python",
    "data scientist":   "Python",
    "machine learning": "Python",
    "devops":           "Bash/Python/YAML",
    "mobile":           "Swift/Kotlin",
    "cloud":            "Python/YAML",
    "security":         "Python",
    "software engineer":"Python",
}

def get_language(position: str) -> str:
    pos_lower = position.lower()
    for key, lang in POSITION_LANGUAGE.items():
        if key in pos_lower:
            return lang
    return "Python"


GENERATION_PROMPT = """\
You are a senior technical interviewer at a top tech company.
Generate exactly {num_questions} interview questions for a **{position}** candidate.
{topics_hint}

Rules:
- Include {mcq_count} MCQ, {bug_count} find-the-bug, {code_count} coding questions
- **Mix in real questions** that have been asked at companies like Google, Amazon, Meta, Microsoft,
  Apple, Netflix, Stripe, Uber, and top startups. For those, add a "company_hint" field
  (e.g. "Asked at Amazon", "Common at FAANG"). Aim for at least half the questions to have a company_hint.
- Order: easiest first, hardest last — strictly increasing difficulty
- Use **{language}** for all code
- MCQ options must all be plausible — no obviously wrong choices
- find_the_bug: provide real buggy code with exactly ONE non-trivial bug
- coding: give a clear problem statement and a starter function template
- Explanations must be thorough (3–5 sentences)
- "remember" must be a single actionable rule/pattern

Respond with ONLY a raw JSON object — no markdown fences, no commentary:

{{
  "questions": [
    {{
      "id": 1,
      "type": "mcq",
      "difficulty": "easy",
      "topic": "<specific topic>",
      "question": "<question text>",
      "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
      "correct_answer": "A) ...",
      "explanation": "<why the correct answer is right and others are wrong>",
      "remember": "<one key rule to remember>",
      "company_hint": "<optional: e.g. 'Asked at Google'>"
    }},
    {{
      "id": 2,
      "type": "find_the_bug",
      "difficulty": "medium",
      "topic": "<specific topic>",
      "question": "Find and fix the bug in the code below:",
      "code": "<buggy code as a string — use \\n for newlines>",
      "language": "<language slug e.g. python>",
      "correct_answer": "<clear description of the bug and the fix>",
      "explanation": "<detailed explanation of why it's a bug and the correct behaviour>",
      "remember": "<one key rule to remember>"
    }},
    {{
      "id": 3,
      "type": "coding",
      "difficulty": "hard",
      "topic": "<specific topic>",
      "question": "<problem statement with input/output examples>",
      "language": "<language slug>",
      "starter_code": "<function/class template with docstring>",
      "correct_answer": "<a complete working solution>",
      "explanation": "<explanation of the optimal approach>",
      "remember": "<one key algorithm/pattern to remember>"
    }}
  ]
}}"""


def _llm_complete(provider: str, api_key: str, prompt: str, max_tokens: int) -> str:
    """Call the appropriate LLM and return the raw text response."""
    if provider == "openai":
        oc = openai_lib.OpenAI(api_key=api_key)
        resp = oc.chat.completions.create(
            model="gpt-4o",
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.choices[0].message.content
    else:
        ac = anthropic.Anthropic(api_key=api_key)
        resp = ac.messages.create(
            model="claude-opus-4-6",
            max_tokens=max_tokens,
            thinking={"type": "adaptive"},
            messages=[{"role": "user", "content": prompt}],
        )
        return next(b.text for b in resp.content if b.type == "text")


def _strip_fences(text: str) -> str:
    if "```json" in text:
        return text.split("```json", 1)[1].split("```", 1)[0].strip()
    if "```" in text:
        return text.split("```", 1)[1].split("```", 1)[0].strip()
    return text


def _claude_cli_complete(prompt: str) -> str:
    """Run claude CLI synchronously and return the text output."""
    import subprocess
    result = subprocess.run(
        [CLAUDE_CLI, "--print", "--output-format", "text", "-p", prompt],
        capture_output=True, text=True, timeout=120,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "claude CLI failed")
    return result.stdout.strip()


def generate_questions(position: str, num_questions: int, custom_topics: Optional[str],
                       provider: str, api_key: str) -> list:
    language = get_language(position)
    mcq_count = max(1, round(num_questions * 0.4))
    code_count = max(1, round(num_questions * 0.3))
    bug_count = num_questions - mcq_count - code_count

    topics_hint = f"Focus specifically on: {custom_topics}." if custom_topics else ""

    prompt = GENERATION_PROMPT.format(
        num_questions=num_questions,
        position=position,
        language=language,
        mcq_count=mcq_count,
        bug_count=bug_count,
        code_count=code_count,
        topics_hint=topics_hint,
    )

    if provider == "claude-cli":
        text = _strip_fences(_claude_cli_complete(prompt))
    else:
        text = _strip_fences(_llm_complete(provider, api_key, prompt, 8000))
    data = json.loads(text)
    return data["questions"]


# ── Answer evaluation ─────────────────────────────────────────────────────────

EVALUATION_PROMPT = """\
Evaluate this technical interview answer.

Question type: {q_type}
Topic: {topic}
Question: {question}
{code_section}
User's answer:
{user_answer}

Expected answer: {correct_answer}

For coding/find_the_bug: the user doesn't need to match exactly — check if they correctly identified \
the core issue or produced a functionally correct solution.

Respond with ONLY a raw JSON object:
{{
  "is_correct": true | false,
  "feedback": "<1-2 sentence immediate verdict>",
  "explanation": "<thorough explanation of the correct answer, 3-5 sentences>",
  "remember": "<the single most important rule/pattern to remember>"
}}"""


def evaluate_answer(question: dict, user_answer: str, provider: str, api_key: str) -> dict:
    q_type = question["type"]

    # MCQ: direct comparison (letter or full text)
    if q_type == "mcq":
        correct = question["correct_answer"].strip()
        user_norm = user_answer.strip().lower()
        correct_norm = correct.lower()
        is_correct = (
            user_norm == correct_norm
            or user_norm == correct_norm[0]
            or correct_norm.startswith(user_norm + ")")
        )
        return {
            "is_correct": is_correct,
            "feedback": "Correct!" if is_correct else f"Incorrect. The answer is: {correct}",
            "explanation": question["explanation"],
            "remember": question["remember"],
        }

    # find_the_bug / coding: use LLM to evaluate
    code_section = ""
    if "code" in question:
        code_section = f"Original buggy code:\n```\n{question['code']}\n```\n"

    prompt = EVALUATION_PROMPT.format(
        q_type=q_type,
        topic=question["topic"],
        question=question["question"],
        code_section=code_section,
        user_answer=user_answer,
        correct_answer=question["correct_answer"],
    )

    text = _strip_fences(_llm_complete(provider, api_key, prompt, 1000))
    return json.loads(text)


def evaluate_answer_claude(question: dict, user_answer: str) -> dict:
    """Evaluate coding/find_the_bug answers using the local claude CLI."""
    code_section = ""
    if "code" in question:
        code_section = f"Original buggy code:\n```\n{question['code']}\n```\n"

    prompt = EVALUATION_PROMPT.format(
        q_type=question["type"],
        topic=question["topic"],
        question=question["question"],
        code_section=code_section,
        user_answer=user_answer,
        correct_answer=question["correct_answer"],
    )
    text = _strip_fences(_claude_cli_complete(prompt))
    return json.loads(text)


SIMILAR_QUESTION_PROMPT = """\
You are a senior technical interviewer. Generate ONE new interview question that tests the \
same core concept and logic as the question below, but with a different scenario or twist.

Original question type: {q_type}
Original topic: {topic}
Original question: {question}
{code_section}
Difficulty: {difficulty}
Language: {language}

Rules:
- Same type ({q_type}), same difficulty, same language
- Different surface scenario — don't just rename variables
- For find_the_bug: introduce a different but equally tricky bug
- For coding: change the input/output structure or add a constraint
- For mcq: change the scenario but test the same underlying concept
- Explanations must be thorough (3-5 sentences)
- "remember" must be a single actionable rule/pattern

Respond with ONLY a raw JSON object (no markdown fences):
{{
  "type": "{q_type}",
  "difficulty": "{difficulty}",
  "topic": "{topic}",
  "question": "<question text>",
  {extra_fields}
  "correct_answer": "<answer>",
  "explanation": "<thorough explanation>",
  "remember": "<key rule>"
}}"""


def generate_similar_question(question: dict) -> dict:
    """Generate a similar question using the local claude CLI."""
    q_type = question["type"]
    language = question.get("language", "python")

    code_section = ""
    if "code" in question:
        code_section = f"Original code:\n```\n{question['code']}\n```\n"
    elif "starter_code" in question:
        code_section = f"Original starter code:\n```\n{question['starter_code']}\n```\n"

    if q_type == "mcq":
        extra_fields = '"options": ["A) ...", "B) ...", "C) ...", "D) ..."],'
    elif q_type == "find_the_bug":
        extra_fields = f'"code": "<buggy code with \\\\n for newlines>", "language": "{language}",'
    else:
        extra_fields = f'"language": "{language}", "starter_code": "<function template>",'

    prompt = SIMILAR_QUESTION_PROMPT.format(
        q_type=q_type,
        topic=question["topic"],
        question=question["question"],
        code_section=code_section,
        difficulty=question["difficulty"],
        language=language,
        extra_fields=extra_fields,
    )
    text = _strip_fences(_claude_cli_complete(prompt))
    new_q = json.loads(text)
    new_q["source"] = "claude-generated"
    return new_q


# ── API routes ────────────────────────────────────────────────────────────────

@app.post("/api/sessions")
async def create_session(req: CreateSessionRequest):
    if not (0 <= req.num_questions <= 20):
        raise HTTPException(400, "num_questions must be between 0 and 20")
    if not req.position.strip():
        raise HTTPException(400, "position is required")
    if req.provider not in ("anthropic", "openai", "claude-cli"):
        raise HTTPException(400, "provider must be 'anthropic', 'openai', or 'claude-cli'")
    # API key only required when using a cloud provider to generate extra questions
    if req.provider in ("anthropic", "openai") and req.num_questions > 0 and not req.api_key.strip():
        raise HTTPException(400, "api_key is required when generating extra questions")

    # Load custom pack questions first
    pack_questions: list[dict] = []
    if req.question_packs:
        all_packs = load_packs()
        for pid in req.question_packs:
            if pid in all_packs:
                pack_questions.extend(all_packs[pid]["questions"])

    # Generate AI questions (skip if num_questions=0)
    generated: list[dict] = []
    if req.num_questions > 0:
        try:
            generated = generate_questions(req.position.strip(), req.num_questions, req.custom_topics,
                                           req.provider, req.api_key.strip())
        except json.JSONDecodeError as e:
            raise HTTPException(500, f"Failed to parse generated questions: {e}")
        except Exception as e:
            raise HTTPException(500, f"Failed to generate questions: {e}")

    if not pack_questions and not generated:
        raise HTTPException(400, "No questions available — select a pack or set num_questions > 0")

    # Merge + sort by difficulty (easy → medium → hard), pack questions first within each tier
    _diff = {"easy": 0, "medium": 1, "hard": 2}
    all_questions = pack_questions + generated
    all_questions.sort(key=lambda q: _diff.get(q.get("difficulty", "medium"), 1))

    # Re-number
    for i, q in enumerate(all_questions):
        q["id"] = i + 1

    # Collect concepts from selected packs (in order)
    concepts: list[dict] = []
    if req.question_packs:
        all_packs = load_packs()
        for pid in req.question_packs:
            if pid in all_packs:
                concepts.extend(all_packs[pid].get("concepts", []))

    session_id = str(uuid.uuid4())
    with get_db() as db:
        db.execute(
            "INSERT INTO sessions (id, position, questions, created_at, provider, api_key) VALUES (?, ?, ?, ?, ?, ?)",
            (session_id, req.position.strip(), json.dumps(all_questions),
             datetime.utcnow().isoformat(), req.provider, req.api_key.strip()),
        )

    return {
        "session_id":    session_id,
        "num_questions": len(all_questions),
        "from_packs":    len(pack_questions),
        "generated":     len(generated),
        "concepts":      concepts,
    }


@app.get("/api/sessions/{session_id}")
async def get_session(session_id: str):
    with get_db() as db:
        session = db.execute("SELECT * FROM sessions WHERE id = ?", (session_id,)).fetchone()
        if not session:
            raise HTTPException(404, "Session not found")
        answers = db.execute(
            "SELECT question_index, is_correct, feedback, user_answer FROM answers "
            "WHERE session_id = ? ORDER BY question_index",
            (session_id,),
        ).fetchall()
        deferred = db.execute(
            "SELECT question_index FROM deferred WHERE session_id = ?", (session_id,)
        ).fetchall()

    questions = json.loads(session["questions"])

    # Strip answer keys before sending to client
    HIDDEN = {"correct_answer", "explanation", "remember"}
    safe_questions = [{k: v for k, v in q.items() if k not in HIDDEN} for q in questions]

    return {
        "session_id": session_id,
        "position": session["position"],
        "questions": safe_questions,
        "answers": [dict(r) for r in answers],
        "deferred": [r["question_index"] for r in deferred],
    }


@app.post("/api/sessions/{session_id}/answer")
async def submit_answer(session_id: str, req: SubmitAnswerRequest):
    with get_db() as db:
        session = db.execute("SELECT * FROM sessions WHERE id = ?", (session_id,)).fetchone()
        if not session:
            raise HTTPException(404, "Session not found")
        existing = db.execute(
            "SELECT id FROM answers WHERE session_id = ? AND question_index = ?",
            (session_id, req.question_index),
        ).fetchone()
        if existing:
            raise HTTPException(400, "Already answered")

    questions = json.loads(session["questions"])
    if req.question_index >= len(questions):
        raise HTTPException(400, "Invalid question index")

    try:
        q = questions[req.question_index]
        if q["type"] in ("find_the_bug", "coding"):
            # Use local claude CLI — free, no API cost
            result = evaluate_answer_claude(q, req.user_answer)
        else:
            result = evaluate_answer(q, req.user_answer, session["provider"], session["api_key"])
    except Exception as e:
        raise HTTPException(500, f"Evaluation failed: {e}")

    with get_db() as db:
        db.execute(
            "INSERT INTO answers (session_id, question_index, user_answer, is_correct, feedback, submitted_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (
                session_id,
                req.question_index,
                req.user_answer,
                int(result["is_correct"]),
                json.dumps(result),
                datetime.utcnow().isoformat(),
            ),
        )

    return result


@app.post("/api/sessions/{session_id}/defer")
async def defer_question(session_id: str, req: DeferRequest):
    with get_db() as db:
        session = db.execute("SELECT id FROM sessions WHERE id = ?", (session_id,)).fetchone()
        if not session:
            raise HTTPException(404, "Session not found")
        already_answered = db.execute(
            "SELECT id FROM answers WHERE session_id = ? AND question_index = ?",
            (session_id, req.question_index),
        ).fetchone()
        if already_answered:
            raise HTTPException(400, "Question already answered")
        db.execute(
            "INSERT OR IGNORE INTO deferred (session_id, question_index) VALUES (?, ?)",
            (session_id, req.question_index),
        )
    return {"deferred": True}


@app.delete("/api/sessions/{session_id}/answer/{question_index}")
async def delete_answer(session_id: str, question_index: int):
    """Allow retrying a question by deleting the previous answer."""
    with get_db() as db:
        session = db.execute("SELECT id FROM sessions WHERE id = ?", (session_id,)).fetchone()
        if not session:
            raise HTTPException(404, "Session not found")
        db.execute(
            "DELETE FROM answers WHERE session_id = ? AND question_index = ?",
            (session_id, question_index),
        )
    return {"deleted": True}


@app.delete("/api/sessions/{session_id}/defer/{question_index}")
async def undefer_question(session_id: str, question_index: int):
    with get_db() as db:
        db.execute(
            "DELETE FROM deferred WHERE session_id = ? AND question_index = ?",
            (session_id, question_index),
        )
    return {"undeferred": True}


class SimilarQuestionRequest(BaseModel):
    question_index: int  # index into session questions (concept-offset already applied by client)

@app.post("/api/sessions/{session_id}/similar")
async def get_similar_question(session_id: str, req: SimilarQuestionRequest):
    """Generate a similar question to the one at question_index using the local claude CLI."""
    with get_db() as db:
        session = db.execute("SELECT * FROM sessions WHERE id = ?", (session_id,)).fetchone()
        if not session:
            raise HTTPException(404, "Session not found")

    questions = json.loads(session["questions"])
    if req.question_index >= len(questions):
        raise HTTPException(400, "Invalid question index")

    original = questions[req.question_index]
    if original.get("type") not in ("mcq", "find_the_bug", "coding"):
        raise HTTPException(400, "Can only generate similar questions for mcq/find_the_bug/coding")

    try:
        new_q = generate_similar_question(original)
    except Exception as e:
        raise HTTPException(500, f"Failed to generate similar question: {e}")

    # Validate it has the required fields
    err = _validate_q(new_q)
    if err:
        raise HTTPException(500, f"Generated question invalid: {err}")

    # Append to the session's question list and persist
    new_q["id"] = len(questions) + 1
    questions.append(new_q)
    with get_db() as db:
        db.execute("UPDATE sessions SET questions = ? WHERE id = ?",
                   (json.dumps(questions), session_id))

    # Return the new question (strip answer fields for client)
    HIDDEN = {"correct_answer", "explanation", "remember"}
    safe_q = {k: v for k, v in new_q.items() if k not in HIDDEN}
    return {"question": safe_q, "index": len(questions) - 1}


@app.get("/api/sessions/{session_id}/summary")
async def get_summary(session_id: str):
    with get_db() as db:
        session = db.execute("SELECT * FROM sessions WHERE id = ?", (session_id,)).fetchone()
        if not session:
            raise HTTPException(404, "Session not found")
        answers = db.execute(
            "SELECT * FROM answers WHERE session_id = ? ORDER BY question_index",
            (session_id,),
        ).fetchall()
        deferred_rows = db.execute(
            "SELECT question_index FROM deferred WHERE session_id = ?", (session_id,)
        ).fetchall()

    questions = json.loads(session["questions"])
    deferred_indices = {r["question_index"] for r in deferred_rows}
    review = []
    for a in answers:
        q = questions[a["question_index"]]
        fb = json.loads(a["feedback"]) if a["feedback"] else {}
        review.append({
            "question_index": a["question_index"],
            "type": q["type"],
            "difficulty": q["difficulty"],
            "topic": q["topic"],
            "question": q["question"],
            "code": q.get("code"),
            "language": q.get("language", "python"),
            "options": q.get("options"),
            "user_answer": a["user_answer"],
            "is_correct": bool(a["is_correct"]),
            "correct_answer": q["correct_answer"],
            "explanation": fb.get("explanation", q.get("explanation", "")),
            "remember": fb.get("remember", q.get("remember", "")),
        })

    # Also include deferred-but-unanswered questions in review
    answered_indices = {a["question_index"] for a in answers}
    for idx in sorted(deferred_indices):
        if idx not in answered_indices:
            q = questions[idx]
            review.append({
                "question_index": idx,
                "type": q["type"],
                "difficulty": q["difficulty"],
                "topic": q["topic"],
                "question": q["question"],
                "code": q.get("code"),
                "language": q.get("language", "python"),
                "options": q.get("options"),
                "user_answer": "(skipped — do later)",
                "is_correct": False,
                "correct_answer": q["correct_answer"],
                "explanation": q.get("explanation", ""),
                "remember": q.get("remember", ""),
                "deferred": True,
            })
    review.sort(key=lambda r: r["question_index"])

    correct = sum(1 for a in answers if a["is_correct"])
    return {
        "session_id": session_id,
        "position": session["position"],
        "total": len(questions),
        "answered": len(answers),
        "deferred": len(deferred_indices - answered_indices),
        "correct": correct,
        "score_pct": round(correct / len(answers) * 100) if answers else 0,
        "review": review,
    }


# ── Claude Code chat ──────────────────────────────────────────────────────────

CLAUDE_CLI = "/Users/sambhus/.local/bin/claude"

CHAT_SYSTEM = """\
You are a focused interview prep tutor embedded in a coding interview portal.
The user is a Java-background engineer learning Python and DSA for technical interviews.

Your role:
- Answer questions about the current concept or coding question shown in context
- Give hints, not full answers — guide reasoning, don't just solve it
- Draw Java parallels when explaining Python concepts
- Keep responses concise and interview-focused
- If asked for the answer directly, give a small nudge instead, then ask if they want the full reveal

You will receive the current question/concept as context at the start of each conversation."""


class ChatMessage(BaseModel):
    role: str   # "user" | "assistant"
    content: str

class ChatRequest(BaseModel):
    context: str          # current question/concept text
    messages: list[ChatMessage]


@app.post("/api/chat")
async def chat(req: ChatRequest):
    """Stream a Claude Code CLI response for the chat panel."""

    # Build the full prompt: system context + conversation history
    history_text = "\n".join(
        f"{'User' if m.role == 'user' else 'Assistant'}: {m.content}"
        for m in req.messages[:-1]  # all but the last (which is the new user message)
    )
    last_user_msg = req.messages[-1].content if req.messages else ""

    prompt = f"{CHAT_SYSTEM}\n\n--- Current question/concept ---\n{req.context}\n"
    if history_text:
        prompt += f"\n--- Conversation so far ---\n{history_text}\n"
    prompt += f"\n--- User asks ---\n{last_user_msg}"

    async def generate():
        try:
            proc = await asyncio.create_subprocess_exec(
                CLAUDE_CLI, "--print", "--output-format", "text", "-p", prompt,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            # Stream stdout chunks as they arrive
            while True:
                chunk = await proc.stdout.read(256)
                if not chunk:
                    break
                text = chunk.decode("utf-8", errors="replace")
                yield f"data: {json.dumps({'text': text})}\n\n"
            await proc.wait()
            yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
            yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream",
                             headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


# ── Static files (no-cache for development) ───────────────────────────────────

class RunCodeRequest(BaseModel):
    code: str
    language: str = "python"


@app.post("/api/run")
async def run_code(req: RunCodeRequest):
    """Execute user Python code in a sandboxed subprocess and return stdout/stderr."""
    if req.language != "python":
        return {"stdout": "", "stderr": f"Only Python execution is supported.", "exit_code": 1}
    try:
        proc = await asyncio.create_subprocess_exec(
            "python3", "-c", req.code,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        try:
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=10)
        except asyncio.TimeoutError:
            proc.kill()
            return {"stdout": "", "stderr": "Execution timed out (10s limit).", "exit_code": 1}
        return {
            "stdout": stdout.decode("utf-8", errors="replace"),
            "stderr": stderr.decode("utf-8", errors="replace"),
            "exit_code": proc.returncode,
        }
    except Exception as e:
        return {"stdout": "", "stderr": str(e), "exit_code": 1}


@app.get("/static/{filename:path}")
async def static_files(filename: str):
    file_path = BASE_DIR / "static" / filename
    if not file_path.exists():
        raise HTTPException(404)
    response = FileResponse(file_path)
    response.headers["Cache-Control"] = "no-store"
    return response

@app.get("/")
async def root():
    response = FileResponse(BASE_DIR / "static" / "index.html")
    response.headers["Cache-Control"] = "no-store"
    return response


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
