import base64
import json
import os
import subprocess
import tempfile

import anthropic
import openai as openai_lib
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

CLAUDE_CLI = os.getenv("CLAUDE_CLI_PATH", "/Users/sambhus/.local/bin/claude")
ANTHROPIC_MODEL = "claude-sonnet-4-20250514"
OPENAI_MODEL = "gpt-4o"


# ---------- low-level completions ----------

def _strip_fences(text: str) -> str:
    if "```json" in text:
        return text.split("```json", 1)[1].split("```", 1)[0].strip()
    if "```" in text:
        return text.split("```", 1)[1].split("```", 1)[0].strip()
    return text.strip()


def _cli_env():
    env = os.environ.copy()
    env.pop("ANTHROPIC_API_KEY", None)
    env.pop("ANTHROPIC_AUTH_TOKEN", None)
    return env


def _complete(prompt: str, max_tokens: int, provider: str, api_key: str) -> str:
    """Route to the correct LLM based on provider."""
    if provider == "claude-cli":
        result = subprocess.run(
            [CLAUDE_CLI, "--print", "--output-format", "text", "--dangerously-skip-permissions"],
            input=prompt,
            capture_output=True, text=True, timeout=180,
            env=_cli_env(),
        )
        if result.returncode != 0:
            err = result.stderr.strip() or result.stdout.strip() or "claude CLI failed with no output"
            raise RuntimeError(f"claude-cli error (rc={result.returncode}): {err}")
        return result.stdout.strip()

    if provider == "openai":
        client = openai_lib.OpenAI(api_key=api_key)
        resp = client.chat.completions.create(
            model=OPENAI_MODEL,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.choices[0].message.content

    # default: anthropic
    client = anthropic.Anthropic(api_key=api_key)
    resp = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.content[0].text


def _complete_json(prompt: str, max_tokens: int, provider: str, api_key: str) -> dict | list:
    raw = _complete(prompt, max_tokens, provider, api_key)
    return json.loads(_strip_fences(raw))


# ---------- image extraction ----------

IMAGE_PROMPT = """This is a photo or screenshot of a math problem from an RSM (Russian School of Mathematics) textbook or worksheet.

Extract the FULL problem text exactly as written. Include:
- The problem number if visible
- All parts (a, b, c, d...) if present
- All numbers, variables, and mathematical expressions (use plain text: x^2, sqrt(), fractions as a/b)
- Any given information, diagrams described in words, or tables

Return ONLY the problem text — no commentary, no "The problem says", no formatting. Just the raw problem."""


def extract_text_from_image(image_b64: str, media_type: str, provider: str, api_key: str) -> str:
    """Use vision to OCR a math problem image."""

    if provider == "openai":
        client = openai_lib.OpenAI(api_key=api_key)
        resp = client.chat.completions.create(
            model=OPENAI_MODEL,
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:{media_type};base64,{image_b64}"}},
                    {"type": "text", "text": IMAGE_PROMPT},
                ],
            }],
        )
        return resp.choices[0].message.content.strip()

    if provider == "claude-cli":
        # Save image to a temp file; tell the CLI to read it
        suffix = ".png" if "png" in media_type else ".jpg"
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as f:
            f.write(base64.b64decode(image_b64))
            tmp_path = f.name
        try:
            prompt = f"{IMAGE_PROMPT}\n\nThe image is saved at: {tmp_path}\nUse your file-reading ability to look at it and extract the problem text."
            result = subprocess.run(
                [CLAUDE_CLI, "--print", "--output-format", "text",
                 "--dangerously-skip-permissions", "--add-dir", tempfile.gettempdir()],
                input=prompt,
                capture_output=True, text=True, timeout=180,
                env=_cli_env(),
            )
            if result.returncode != 0:
                err = result.stderr.strip() or "claude CLI failed"
                raise RuntimeError(f"claude-cli error: {err}")
            return result.stdout.strip()
        finally:
            os.unlink(tmp_path)

    # anthropic (default)
    client = anthropic.Anthropic(api_key=api_key)
    resp = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": image_b64}},
                {"type": "text", "text": IMAGE_PROMPT},
            ],
        }],
    )
    return resp.content[0].text.strip()


# ---------- similar question generation ----------

def generate_similar_question(question_text: str, provider: str, api_key: str) -> dict:
    """Generate a new practice question similar in style and difficulty."""
    prompt = f"""You are an RSM math tutor. A student has just worked on this problem:

ORIGINAL PROBLEM:
{question_text}

Create ONE new practice problem that:
- Tests the same mathematical concept and skill
- Is similar in difficulty
- Uses different numbers, names, or scenario so it feels fresh
- Is clearly worded and self-contained (no references to the original)

Respond ONLY with valid JSON:
{{
  "text": "The full new problem statement"
}}

No markdown fences, no explanation."""

    return _complete_json(prompt, 512, provider, api_key)


# ---------- feature functions ----------

def extract_questions_from_text(pdf_text: str, provider: str, api_key: str) -> list[dict]:
    prompt = f"""You are an expert math tutor analyzing RSM (Russian School of Mathematics) homework.

Below is text extracted from a homework PDF. Identify and extract each individual math problem/question.

PDF TEXT:
{pdf_text}

Extract all math problems. Return a JSON array where each element has:
- "number": problem number or label (string, e.g. "1", "2a", "Problem 3")
- "text": the full problem statement (string)

Rules:
- Include ALL problems, even similar-looking ones
- Preserve math notation using plain text (x^2 for x squared, sqrt() for square root)
- Treat each sub-part (a, b, c) as a separate question
- Do NOT include answers, hints, or solutions

Respond ONLY with a valid JSON array, no explanation or markdown fences."""

    return _complete_json(prompt, 4096, provider, api_key)


def generate_hints_and_solution(question_text: str, provider: str, api_key: str) -> dict:
    prompt = f"""You are an expert RSM math tutor. Given this math problem, generate:
1. Three progressive Socratic hints (guiding without giving away the answer)
2. A complete step-by-step RSM-style solution

PROBLEM:
{question_text}

Respond ONLY with valid JSON in this exact format:
{{
  "hint1": "Conceptual nudge — what type of problem is this or what concept applies",
  "hint2": "Setup guidance — suggest drawing a diagram, setting up variables, or identifying given info",
  "hint3": "Show the very first concrete step or equation to write down",
  "solution": "Full step-by-step solution with clear numbered steps and explanations"
}}

Rules for hints:
- hint1: Pure conceptual, no math yet
- hint2: Help set up the problem
- hint3: Show the actual first step explicitly — but NOT the final answer
- Keep hints encouraging and age-appropriate for a middle school student

Rules for solution:
- Number each step clearly, show all work, explain WHY each step is taken
- State the final answer clearly at the end

Respond ONLY with valid JSON, no markdown fences."""

    return _complete_json(prompt, 2048, provider, api_key)


def check_student_answer(question_text: str, student_answer: str, provider: str, api_key: str,
                          known_solution: str = "") -> dict:
    solution_block = f"""
CORRECT SOLUTION (use this as the definitive answer — do NOT re-solve):
{known_solution}
""" if known_solution else ""

    prompt = f"""You are an encouraging RSM math tutor checking a student's answer.

PROBLEM:
{question_text}
{solution_block}
STUDENT'S ANSWER:
{student_answer}

Compare the student's answer to the correct solution above.
Accept equivalent forms (120 km/h = 120 km/hr, 1/2 = 0.5 = 50%, etc.).

Respond ONLY with valid JSON:
{{
  "correct": true or false,
  "feedback": "Encouraging feedback message (2-3 sentences)",
  "correct_answer": "The correct final answer (brief, just the value)"
}}

Rules:
- If correct: celebrate enthusiastically!
- If incorrect: be gentle, point toward what to reconsider without giving away the answer.
- Keep feedback age-appropriate for a middle school student.

Respond ONLY with valid JSON, no markdown fences."""

    return _complete_json(prompt, 512, provider, api_key)
