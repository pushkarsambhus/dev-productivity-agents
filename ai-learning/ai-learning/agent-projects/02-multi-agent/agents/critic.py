"""
agents/critic.py — The Critic sub-agent.

ROLE: Review a draft and return actionable improvement suggestions.
      Optionally decide whether the draft is good enough to publish.

LEARNING NOTE — Why have a Critic?
    Large language models are good at generating plausible text,
    but they can also:
      • Hallucinate facts
      • Lose track of the user's original goal
      • Write verbosely or with poor structure
      • Miss important caveats

    A separate Critic pass adds a "check" to the pipeline.
    This is an example of the REFLECTION pattern in agentic AI:
      1. Generate something (Writer)
      2. Reflect on it critically (Critic)
      3. Improve based on feedback (Writer again)

    TRADE-OFF:
      + Catches errors and improves quality
      + Mirrors human writing/editing workflow
      - Adds an extra API call (cost + latency)
      - The Critic itself can be wrong or overly strict
      - Creates a loop: how do you know when to stop revising?
        (We cap at MAX_REVISION_ROUNDS in config.py)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from typing import Optional
import provider as prov
import config


CRITIC_SYSTEM_PROMPT = """You are an expert editor and fact-checker.

You receive:
  1. The original user request
  2. The research brief (what facts are available)
  3. A draft document

Your job is to return a structured critique with:

SECTION 1 — VERDICT
  "APPROVE" if the draft is good enough to publish as-is.
  "REVISE"  if it needs changes.

SECTION 2 — ISSUES (only if REVISE)
  A numbered list of specific problems. For each:
    - What is wrong
    - Where (quote a few words from the draft)
    - How to fix it

SECTION 3 — STRENGTHS (always)
  What the draft does well.

Be constructive and specific. Vague feedback like "improve the writing"
is not useful. Instead: "Paragraph 2 sentence 3 is unclear — rephrase as..."
"""


def run_critic(
    user_request: str,
    research_brief: str,
    draft: str,
) -> dict:
    """
    Review a draft and return a structured critique.

    Returns
    -------
    dict with keys:
        verdict : "APPROVE" | "REVISE"
        feedback : str  — the full critique text
        approve  : bool — True if APPROVE
    """
    api_key = config.ANTHROPIC_API_KEY if config.PROVIDER == "anthropic" else config.OPENAI_API_KEY
    model   = config.CRITIC_MODEL if config.PROVIDER == "anthropic" else config.CRITIC_MODEL_OPENAI
    client  = prov.create_client(config.PROVIDER, api_key)

    messages: list[dict] = [
        {
            "role": "user",
            "content": (
                f"USER REQUEST:\n{user_request}\n\n"
                f"RESEARCH BRIEF:\n{research_brief}\n\n"
                f"DRAFT TO REVIEW:\n{draft}\n\n"
                "Please provide your critique."
            ),
        }
    ]

    if config.VERBOSE:
        print(f"\n  [CRITIC] Reviewing draft ({len(draft)} chars)...")

    response = prov.call_api(
        client=client,
        provider=config.PROVIDER,
        model=model,
        max_tokens=config.MAX_TOKENS_PER_AGENT,
        system=CRITIC_SYSTEM_PROMPT,
        tools=None,
        messages=messages,
    )

    feedback_text = _extract_text(response.content)

    # Determine verdict from the text
    # TRADE-OFF: simple string check vs. structured output.
    # For production: use output_config with a JSON schema to guarantee
    # structured output. Here we keep it simple for learning.
    verdict_line = feedback_text.upper()
    approve = "APPROVE" in verdict_line[:200]  # Check early in response

    if config.VERBOSE:
        verdict_str = "APPROVED ✓" if approve else "NEEDS REVISION ↺"
        print(f"  [CRITIC] Verdict: {verdict_str}")

    return {
        "verdict": "APPROVE" if approve else "REVISE",
        "feedback": feedback_text,
        "approve": approve,
    }


def _extract_text(content_blocks) -> str:
    return "\n".join(
        getattr(b, "text", b.get("text", ""))
        for b in content_blocks
        if (getattr(b, "type", b.get("type")) == "text")
    ).strip()
