# 🎯 Interview Prep Portal

A locally-hosted, AI-powered technical interview practice tool.  
Questions are generated on-demand by an AI model of your choice based on your target role — or loaded from your own `.py` question packs.

---

## Features

- **Provider choice** — use Anthropic (Claude) or OpenAI (GPT-4o); enter your API key directly in the UI
- **Three question types** — MCQ, Find the Bug, and Coding challenges
- **Increasing difficulty** — questions are ordered easy → medium → hard every session
- **Role-aware generation** — questions are tailored to the specific position (languages, frameworks, domain concepts)
- **Wrong-answer feedback** — every incorrect answer shows a full explanation + a "💡 Remember" tip
- **Custom question packs** — drop a `.py` file into `custom_questions/` to inject your own questions
- **Session persistence** — progress is saved in SQLite and resumes on page refresh
- **Monaco Editor** — full IDE-quality code editor for coding and find-the-bug questions

---

## Quick Start

### 1. Install dependencies

```bash
cd interview-portal
uv pip install -r requirements.txt
```

> Don't have `uv`? Install it with `pip install uv` or `curl -LsSf https://astral.sh/uv/install.sh | sh`

### 2. Run the server

```bash
python app.py
```

### 3. Open the portal

```
http://localhost:8000
```

### 4. Enter your API key in the UI

On the landing page, select your AI provider and paste your key into the **API Key** field before starting a session.

| Provider | Key format | Where to get one |
|---|---|---|
| Anthropic | `sk-ant-…` | console.anthropic.com |
| OpenAI | `sk-…` | platform.openai.com |

Your key is sent directly to the backend per request and is never stored in the browser.

---

## Project Structure

```
interview-portal/
├── app.py                        # FastAPI backend
├── requirements.txt
├── sessions.db                   # SQLite — created automatically on first run
├── custom_questions/             # Drop your own .py packs here
│   ├── example_ai_ml.py          # Bundled pack: AI / ML Engineering
│   └── example_red_team.py       # Bundled pack: Red Team Engineering
└── static/
    ├── index.html
    ├── style.css
    └── app.js
```

---

## Target Roles

The landing page has preset cards for these roles (pinned at the top):

| Role | Focus areas |
|---|---|
| 🤖 AI / ML Engineer | LLMs, fine-tuning, MLOps, PyTorch, evals |
| 🎯 AI Platform & Evaluation | Eval frameworks, benchmarking, RAG quality, LLM observability |
| 🔴 Red Team Engineer | Adversarial ML, prompt injection, jailbreaks, MITRE ATT&CK |
| 🤝 Product Manager | PRDs, metrics, prioritisation, stakeholder management |
| 🧪 AI Automation Test Engineer | LLM test harnesses, eval pipelines, pytest, CI |
| 👔 Engineering Manager | Team leadership, delivery, hiring, OKRs |
| 📋 Technical Program Manager | Cross-team programs, risk management, exec communication |

Plus general roles: Frontend, Backend, Data Scientist, DevOps, Cloud Architect, Security Engineer, Software Engineer.

You can also type **any custom role** in the free-text field.

---

## Question Types

### MCQ
Four plausible options — no obviously wrong choices. Evaluated by direct string match.

### Find the Bug
A code snippet with exactly one non-trivial bug. Rendered in a Monaco editor — **edit the code directly** to fix it, then submit. Claude evaluates whether your fix addresses the core issue.

### Coding
A problem statement with examples and a starter function template. Write your solution in the Monaco editor and submit. Claude evaluates functional correctness, not exact text match.

---

## Custom Question Packs

Create a `.py` file in `custom_questions/` — it appears as a toggle card on the landing page.  
Selected packs are **added on top of** the AI-generated questions and sorted by difficulty.

### Minimal template

```python
NAME        = "My Pack"
DESCRIPTION = "Short description shown on the card"
ICON        = "🧠"          # any emoji

QUESTIONS = [
    {
        "type":           "mcq",       # mcq | find_the_bug | coding
        "difficulty":     "medium",    # easy | medium | hard
        "topic":          "Topic Name",
        "question":       "Question text",
        "options":        ["A) ...", "B) ...", "C) ...", "D) ..."],
        "correct_answer": "A) ...",
        "explanation":    "Full explanation shown after answering.",
        "remember":       "The one key rule to remember.",
    },
]
```

### Find the Bug question

```python
{
    "type":           "find_the_bug",
    "difficulty":     "hard",
    "topic":          "Async/Await",
    "question":       "Find and fix the bug in this code:",
    "code":           "async def fetch():\n    return requests.get(url)",  # use \n for newlines
    "language":       "python",
    "correct_answer": "requests.get() is synchronous — use aiohttp or httpx instead.",
    "explanation":    "Calling a blocking function inside async...",
    "remember":       "Never call blocking I/O inside an async function.",
}
```

### Coding question

```python
{
    "type":           "coding",
    "difficulty":     "hard",
    "topic":          "Binary Search",
    "question":       "Implement binary search.\n\nExample:\n  search([1,3,5,7], 5) → 2",
    "language":       "python",
    "starter_code":   "def search(arr: list, target: int) -> int:\n    pass",
    "correct_answer": "def search(arr, target):\n    lo, hi = 0, len(arr)-1\n    ...",
    "explanation":    "Binary search halves the search space each step — O(log n).",
    "remember":       "Binary search: O(log n). Requires a sorted array.",
}
```

### Required fields for all question types

| Field | Type | Notes |
|---|---|---|
| `type` | str | `mcq`, `find_the_bug`, or `coding` |
| `difficulty` | str | `easy`, `medium`, or `hard` |
| `topic` | str | Shown as a tag on the question card |
| `question` | str | The question text |
| `correct_answer` | str | Used for evaluation and shown in the summary |
| `explanation` | str | Shown after answering (correct or wrong) |
| `remember` | str | One-line key insight shown in the 💡 tip |

**MCQ extras:** `options` (list of 4 strings, prefixed `A) … B) …`)  
**Find the Bug extras:** `code` (str, use `\n` for newlines), `language` (str, e.g. `python`)  
**Coding extras:** `language` (str), `starter_code` (str)

### Validation

The server validates every question when a pack is loaded. Invalid questions are skipped and a warning is shown on the card. The server log prints details.

---

## Configuration

| Setting | Where | Default |
|---|---|---|
| AI provider | Landing page toggle (Anthropic / OpenAI) | Anthropic |
| API key | Landing page key field | — (required) |
| Number of questions | Landing page toggle (5 / 10 / 15) | 10 |
| Custom topics | Landing page text field | None |
| Question packs | Landing page toggle cards | None selected |
| Server port | `app.py` → `uvicorn.run(port=...)` | 8000 |
| Model (Anthropic) | `app.py` → `_llm_complete()` | `claude-opus-4-6` |
| Model (OpenAI) | `app.py` → `_llm_complete()` | `gpt-4o` |

---

## API Reference

| Method | Path | Description |
|---|---|---|
| `GET` | `/` | Serves the frontend |
| `GET` | `/api/question-packs` | Lists all loaded `.py` packs |
| `POST` | `/api/sessions` | Creates a session, generates questions |
| `GET` | `/api/sessions/{id}` | Returns session state (answers hidden) |
| `POST` | `/api/sessions/{id}/answer` | Submits an answer, returns evaluation |
| `GET` | `/api/sessions/{id}/summary` | Returns full results with explanations |

### POST `/api/sessions` body

```json
{
  "position":       "Red Team Engineer",
  "num_questions":  10,
  "custom_topics":  "Active Directory, Kerberoasting",
  "question_packs": ["example_red_team"],
  "provider":       "anthropic",
  "api_key":        "sk-ant-..."
}
```

`provider` must be `"anthropic"` or `"openai"`. `api_key` is required.

---

## How Evaluation Works

| Type | How |
|---|---|
| MCQ | Direct string comparison (letter or full option text) |
| Find the Bug | Claude compares your fixed code against the expected fix — partial credit for correct identification |
| Coding | Claude evaluates functional correctness — exact wording doesn't matter |

---

## Bundled Question Packs

### `example_ai_ml.py` — AI / ML Engineering (6 questions)

| # | Type | Difficulty | Topic |
|---|---|---|---|
| 1 | MCQ | Easy | Transformer attention scaling |
| 2 | MCQ | Easy | Tokenisation / BPE |
| 3 | MCQ | Medium | LoRA fine-tuning |
| 4 | Find the Bug | Medium | PyTorch training loop (missing `zero_grad`) |
| 5 | MCQ | Hard | RLHF KL divergence penalty |
| 6 | Coding | Hard | Perplexity from scratch |

### `example_red_team.py` — Red Team Engineering (5 questions)

| # | Type | Difficulty | Topic |
|---|---|---|---|
| 1 | MCQ | Easy | Direct vs indirect prompt injection |
| 2 | Find the Bug | Medium | LLM-assisted RCE via `subprocess` |
| 3 | MCQ | Medium | Jailbreak techniques (persona/DAN) |
| 4 | MCQ | Hard | Sleeper agent vs jailbreak distinction |
| 5 | Coding | Hard | Heuristic prompt-injection detector |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python · FastAPI · Uvicorn |
| AI | Anthropic Claude (`claude-opus-4-6`) or OpenAI (`gpt-4o`) — your choice |
| Database | SQLite (built-in, zero config) |
| Frontend | Vanilla HTML / CSS / JavaScript |
| Code editor | Monaco Editor (CDN) |
| Fonts | Inter · JetBrains Mono (Google Fonts) |
