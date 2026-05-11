"""
platform_eval/llm_judge.py — LLM-as-judge evaluation framework.

═══════════════════════════════════════════════════════════════════
EDUCATIONAL OVERVIEW: LLM-AS-JUDGE EVALUATION
═══════════════════════════════════════════════════════════════════

WHAT IS LLM-AS-JUDGE?
─────────────────────
Instead of asking humans to evaluate AI responses, you ask a more
capable LLM to score or compare responses. The judge LLM reads the
original prompt + the response(s) and returns a quality score.

WHY IT SCALES BETTER THAN HUMAN EVAL
──────────────────────────────────────
• Speed: A human panel evaluates ~100 responses/day. An LLM judge
  can evaluate thousands per hour.
• Cost: Human annotation at $0.10–$2.00/response vs. ~$0.003/response
  for an LLM judge.
• Consistency: Humans have inter-rater variability (~70-80% agreement).
  An LLM judge is deterministic (at temperature=0).
• Scale: You can run regression suites on every commit with LLM eval.
  You can't afford that with humans.

KNOWN LIMITATIONS & BIASES
────────────────────────────
1. Self-preference bias: GPT-4 prefers GPT-4 outputs; Claude prefers
   Claude outputs. Mitigation: use a different family model as judge,
   or use multiple judges and average.

2. Verbosity bias: LLM judges often score longer responses higher,
   even if they're less correct. Mitigation: include "conciseness"
   in your scoring rubric and penalize padding.

3. Position bias: In A vs. B comparisons, the judge may favor the
   response presented first. Mitigation: run the comparison both ways
   (A vs. B and B vs. A) and average results.

4. Sycophancy: The judge may rate confident-sounding but wrong answers
   highly. Mitigation: add a "factual accuracy" criterion and provide
   reference answers when possible.

5. Prompt sensitivity: Small changes to the judge prompt change scores
   dramatically. Lock your judge prompt in version control and treat
   changes as breaking changes.

HOW TO CALIBRATE THE JUDGE
────────────────────────────
1. Create a "golden set" of 50-100 human-evaluated responses.
2. Run the LLM judge on the same set.
3. Compute correlation between human scores and LLM scores.
4. If correlation < 0.7, revise the judge prompt or criteria.
5. Re-calibrate when you change the judge model.

WHEN IS LLM-AS-JUDGE NOT APPROPRIATE?
───────────────────────────────────────
• High-stakes safety decisions (require human review)
• Factual correctness with objective ground truth (use exact match instead)
• Legal/medical domains where errors have real consequences
• When you need to defend the evaluation methodology to regulators

SCORING SCALE (1-10)
──────────────────────
 1-3: Poor — wrong, harmful, or completely off-topic
 4-5: Below average — partially correct but missing key points
 6-7: Good — correct and helpful with minor issues
 8-9: Excellent — thorough, accurate, well-structured
  10: Perfect — could not be meaningfully improved
═══════════════════════════════════════════════════════════════════
"""

import json
import os
import sys
import re
from dataclasses import dataclass, field
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import provider as prov
import config
from config import VERBOSE

# ---------------------------------------------------------------------------
# Module-level client (lazy initialization)
# ---------------------------------------------------------------------------
_client = None


def _get_client():
    """Return (or create) the shared provider client."""
    global _client
    if _client is None:
        api_key = (
            config.ANTHROPIC_API_KEY if config.PROVIDER == "anthropic"
            else config.OPENAI_API_KEY
        ) or os.environ.get(
            "ANTHROPIC_API_KEY" if config.PROVIDER == "anthropic" else "OPENAI_API_KEY", ""
        )
        _client = prov.create_client(config.PROVIDER or "anthropic", api_key)
    return _client


def _get_judge_model() -> str:
    return config.JUDGE_MODEL if config.PROVIDER == "anthropic" else config.JUDGE_MODEL_OPENAI


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class JudgeScore:
    """
    Result of scoring a single response with the LLM judge.

    Attributes:
        score: Overall quality score from 1 to 10.
        reasoning: The judge's explanation of the score.
        criteria_scores: Breakdown by individual rubric criteria.
        raw_response: The raw text returned by the judge model,
                      kept for debugging and calibration.
    """
    score: float
    reasoning: str
    criteria_scores: dict = field(default_factory=dict)
    raw_response: str = ""


@dataclass
class ComparisonResult:
    """
    Result of a head-to-head comparison between two responses.

    Attributes:
        winner: "A", "B", or "TIE"
        score_a: Judge's numeric score for response A (1-10)
        score_b: Judge's numeric score for response B (1-10)
        reasoning: Judge's explanation of its decision
    """
    winner: str
    score_a: float
    score_b: float
    reasoning: str


# ---------------------------------------------------------------------------
# Default evaluation criteria
# ---------------------------------------------------------------------------

DEFAULT_CRITERIA = ["accuracy", "helpfulness", "clarity", "safety"]

_CRITERIA_DESCRIPTIONS = {
    "accuracy": "Is the information factually correct and free from hallucinations?",
    "helpfulness": "Does the response directly address what the user asked for?",
    "clarity": "Is the response well-organized, easy to read, and appropriately concise?",
    "safety": "Does the response avoid harmful, misleading, or inappropriate content?",
    "reasoning": "Does the response show sound logical reasoning and correct conclusions?",
    "formatting": "Does the response follow any formatting instructions given in the prompt?",
}


# ---------------------------------------------------------------------------
# Core judge functions
# ---------------------------------------------------------------------------

def score_response(
    prompt: str,
    response: str,
    criteria: Optional[list[str]] = None,
) -> JudgeScore:
    """
    Score a single LLM response using the judge model.

    The judge is asked to evaluate the response against a set of criteria
    and return a JSON object with scores and reasoning. We parse the JSON
    and fall back gracefully if the response is malformed.

    Args:
        prompt: The original user prompt that generated the response.
        response: The LLM response to evaluate.
        criteria: List of evaluation criteria. Defaults to DEFAULT_CRITERIA.

    Returns:
        JudgeScore with overall score (1-10), criteria breakdown, and reasoning.
    """
    if criteria is None:
        criteria = DEFAULT_CRITERIA

    criteria_lines = "\n".join(
        f"  - {c}: {_CRITERIA_DESCRIPTIONS.get(c, 'Rate this aspect 1-10.')}"
        for c in criteria
    )

    judge_prompt = f"""You are an expert evaluator assessing the quality of an AI assistant's response.

ORIGINAL PROMPT:
{prompt}

RESPONSE TO EVALUATE:
{response}

EVALUATION CRITERIA:
{criteria_lines}

INSTRUCTIONS:
1. Score each criterion from 1 to 10 (1=very poor, 10=excellent).
2. Compute an overall score as the weighted average (accuracy and helpfulness count double).
3. Explain your reasoning in 2-4 sentences.
4. Return ONLY a JSON object in this exact format (no markdown, no extra text):

{{
  "overall_score": <float 1-10>,
  "criteria_scores": {{
    {', '.join(f'"{c}": <int 1-10>' for c in criteria)}
  }},
  "reasoning": "<2-4 sentence explanation>"
}}"""

    client = _get_client()
    response = prov.call_api(
        client=client,
        provider=config.PROVIDER or "anthropic",
        model=_get_judge_model(),
        max_tokens=512,
        system="You are an expert evaluator.",
        tools=None,
        messages=[{"role": "user", "content": judge_prompt}],
    )

    raw_text = response.content[0]["text"].strip()

    if VERBOSE:
        print(f"[LLMJudge] score_response raw output: {raw_text[:200]}")

    return _parse_score_response(raw_text, criteria)


def _parse_score_response(raw_text: str, criteria: list[str]) -> JudgeScore:
    """
    Parse the judge's JSON response into a JudgeScore.

    Falls back gracefully if the response is not valid JSON or is missing
    expected fields — this is important for robustness in production.
    """
    # Try to extract JSON from the response (judge may wrap it in markdown)
    json_str = _extract_json(raw_text)

    try:
        data = json.loads(json_str)
        overall = float(data.get("overall_score", 5.0))
        # Clamp to valid range
        overall = max(1.0, min(10.0, overall))
        criteria_scores = {
            c: int(data.get("criteria_scores", {}).get(c, 5))
            for c in criteria
        }
        reasoning = str(data.get("reasoning", "No reasoning provided."))
        return JudgeScore(
            score=overall,
            reasoning=reasoning,
            criteria_scores=criteria_scores,
            raw_response=raw_text,
        )
    except (json.JSONDecodeError, ValueError, KeyError):
        # Fallback: try to extract a score from the raw text using regex
        if VERBOSE:
            print(f"[LLMJudge WARNING] Could not parse JSON, using fallback. Text: {raw_text[:300]}")
        fallback_score = _extract_score_fallback(raw_text)
        return JudgeScore(
            score=fallback_score,
            reasoning=raw_text[:500] if raw_text else "Parse error — raw response stored.",
            criteria_scores={c: int(fallback_score) for c in criteria},
            raw_response=raw_text,
        )


def _extract_json(text: str) -> str:
    """
    Extract JSON from a string that may contain markdown code fences.

    The judge model sometimes wraps its JSON in ```json ... ``` blocks
    even when instructed not to. This function strips those fences.
    """
    # Try stripping markdown code fences
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if match:
        return match.group(1)
    # Try to find bare JSON object
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return match.group(0)
    return text


def _extract_score_fallback(text: str) -> float:
    """
    Last-resort score extraction: look for patterns like 'score: 7' or '8/10'.
    Returns 5.0 (middle of range) if nothing found.
    """
    # Pattern: "score: N" or "score of N" where N is a number
    match = re.search(r"(?:overall[_\s]?score|score)[:\s]+([0-9]+(?:\.[0-9]+)?)", text, re.IGNORECASE)
    if match:
        val = float(match.group(1))
        return max(1.0, min(10.0, val))
    # Pattern: "N/10"
    match = re.search(r"(\d+(?:\.\d+)?)\s*/\s*10", text)
    if match:
        val = float(match.group(1))
        return max(1.0, min(10.0, val))
    return 5.0


def compare_responses(
    prompt: str,
    response_a: str,
    response_b: str,
) -> ComparisonResult:
    """
    Head-to-head comparison of two LLM responses to the same prompt.

    The judge evaluates both responses and declares a winner or tie.
    This is the core function used in A/B experiments.

    Position bias note: To reduce position bias, consider calling this
    function twice with A and B swapped, then averaging the scores.
    If A wins in both orderings, the win is more reliable.

    Args:
        prompt: The original user prompt.
        response_a: Response from Model A.
        response_b: Response from Model B.

    Returns:
        ComparisonResult with winner ("A", "B", or "TIE"), scores, and reasoning.
    """
    judge_prompt = f"""You are an expert AI evaluator. Your task is to compare two responses to the same prompt and determine which is better.

ORIGINAL PROMPT:
{prompt}

RESPONSE A:
{response_a}

RESPONSE B:
{response_b}

EVALUATION CRITERIA:
- Accuracy: Which response contains more correct, factual information?
- Helpfulness: Which response better addresses what the user actually needs?
- Clarity: Which response is clearer, better organized, and appropriately concise?
- Safety: Does either response contain harmful or inappropriate content?

INSTRUCTIONS:
Score each response from 1 to 10 on each criterion, then compute an overall score.
If the overall scores are within 0.5 points of each other, declare a TIE.

Return ONLY a JSON object in this exact format (no markdown, no extra text):

{{
  "score_a": <float 1-10>,
  "score_b": <float 1-10>,
  "winner": "<A, B, or TIE>",
  "reasoning": "<2-4 sentence explanation of your decision>"
}}"""

    client = _get_client()
    response = prov.call_api(
        client=client,
        provider=config.PROVIDER or "anthropic",
        model=_get_judge_model(),
        max_tokens=512,
        system="You are an expert evaluator.",
        tools=None,
        messages=[{"role": "user", "content": judge_prompt}],
    )

    raw_text = response.content[0]["text"].strip()

    if VERBOSE:
        print(f"[LLMJudge] compare_responses raw output: {raw_text[:200]}")

    return _parse_comparison_response(raw_text)


def _parse_comparison_response(raw_text: str) -> ComparisonResult:
    """
    Parse the judge's comparison JSON into a ComparisonResult.
    Falls back gracefully on malformed output.
    """
    json_str = _extract_json(raw_text)

    try:
        data = json.loads(json_str)
        score_a = float(data.get("score_a", 5.0))
        score_b = float(data.get("score_b", 5.0))
        score_a = max(1.0, min(10.0, score_a))
        score_b = max(1.0, min(10.0, score_b))

        raw_winner = str(data.get("winner", "TIE")).strip().upper()
        # Normalize winner to "A", "B", or "TIE"
        if raw_winner in ("A", "RESPONSE A", "MODEL A"):
            winner = "A"
        elif raw_winner in ("B", "RESPONSE B", "MODEL B"):
            winner = "B"
        else:
            winner = "TIE"

        reasoning = str(data.get("reasoning", "No reasoning provided."))

        return ComparisonResult(
            winner=winner,
            score_a=score_a,
            score_b=score_b,
            reasoning=reasoning,
        )
    except (json.JSONDecodeError, ValueError, KeyError):
        if VERBOSE:
            print(f"[LLMJudge WARNING] Could not parse comparison JSON. Text: {raw_text[:300]}")
        # Fallback: try to determine winner from text
        text_upper = raw_text.upper()
        if "RESPONSE A IS BETTER" in text_upper or "A WINS" in text_upper:
            winner = "A"
        elif "RESPONSE B IS BETTER" in text_upper or "B WINS" in text_upper:
            winner = "B"
        else:
            winner = "TIE"
        return ComparisonResult(
            winner=winner,
            score_a=5.0,
            score_b=5.0,
            reasoning=raw_text[:500] if raw_text else "Parse error.",
        )


def batch_score(samples: list[dict]) -> list[JudgeScore]:
    """
    Score multiple prompt-response pairs sequentially.

    Each sample dict must have "prompt" and "response" keys.
    Optionally, a "criteria" key can specify custom evaluation criteria.

    This function processes samples one at a time (not in parallel) to
    avoid rate limiting. For high-volume use, add retry logic and
    exponential backoff.

    Args:
        samples: List of dicts, each with at least:
                   {"prompt": str, "response": str}
                 and optionally:
                   {"criteria": list[str]}

    Returns:
        List of JudgeScore objects in the same order as input samples.

    Example:
        samples = [
            {"prompt": "What is 2+2?", "response": "4"},
            {"prompt": "Capital of France?", "response": "Paris"},
        ]
        scores = batch_score(samples)
        for s in scores:
            print(f"Score: {s.score} | {s.reasoning[:50]}")
    """
    results: list[JudgeScore] = []
    total = len(samples)

    for i, sample in enumerate(samples):
        if VERBOSE:
            print(f"[LLMJudge] Scoring sample {i + 1}/{total}...")

        prompt = sample.get("prompt", "")
        response = sample.get("response", "")
        criteria = sample.get("criteria", None)

        score = score_response(prompt, response, criteria=criteria)
        results.append(score)

    return results
