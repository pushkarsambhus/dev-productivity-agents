"""
agents/writer.py — The Writer sub-agent.

ROLE: Turn research findings into a well-structured, readable document.

LEARNING NOTE:
    The Writer receives the Researcher's output as input.
    It does NOT search the web — its job is purely to transform
    raw facts into prose.

    TRADE-OFF: Separating research from writing means:
      + Each agent can be optimized for its task
      + Researcher and Writer can theoretically run in parallel
        (if tasks are independent)
      - Adds coordination overhead (orchestrator must pass data between agents)
      - If the Researcher missed something, the Writer can't fill the gap

    In practice: for simple tasks, a single agent is fine.
    For tasks where quality in each phase matters (journalism, reports,
    technical docs), separation is worth it.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from typing import Optional
import provider as prov
import config


# ─────────────────────────────────────────────────────────────────────────────
# Writer-specific system prompt
# ─────────────────────────────────────────────────────────────────────────────

WRITER_SYSTEM_PROMPT = """You are a skilled writer who turns research into clear, engaging text.

You receive:
  1. A user request (what kind of document to write)
  2. A research brief (facts and sources from the Researcher agent)
  3. Optional critic feedback (if this is a revision round)

OUTPUT FORMAT:
- Write in clear, professional prose
- Use the research facts accurately — do not invent information
- Include an introduction, body paragraphs, and conclusion
- Cite sources inline where relevant (e.g., "According to [source]...")
- Match the tone to the request (formal report vs. casual explanation)

You do NOT need to use any tools — all the information you need is provided.
Focus entirely on writing quality.
"""

# ─────────────────────────────────────────────────────────────────────────────
# The Writer has NO tools (pure text transformation)
# ─────────────────────────────────────────────────────────────────────────────
# TRADE-OFF: No tools → cheaper, faster, no tool-use loop needed.
#            If the Writer needed to look something up, it would need tools.
#            Here we trust the Researcher to provide complete information.

WRITER_TOOLS: list = []


def run_writer(
    user_request: str,
    research_brief: str,
    critic_feedback: Optional[str] = None,
) -> str:
    """
    Write a document based on research and optional critic feedback.

    Parameters
    ----------
    user_request : str
        The original user ask (e.g., "write a 200-word summary of X").
    research_brief : str
        Output from the Researcher agent.
    critic_feedback : str, optional
        If this is a revision, the Critic's specific improvement requests.

    Returns
    -------
    str
        The written document.
    """
    api_key = config.ANTHROPIC_API_KEY if config.PROVIDER == "anthropic" else config.OPENAI_API_KEY
    model   = config.WRITER_MODEL if config.PROVIDER == "anthropic" else config.WRITER_MODEL_OPENAI
    client  = prov.create_client(config.PROVIDER, api_key)

    # Build a structured prompt for the Writer
    content_parts = [
        f"USER REQUEST:\n{user_request}\n",
        f"RESEARCH BRIEF:\n{research_brief}\n",
    ]
    if critic_feedback:
        content_parts.append(
            f"CRITIC FEEDBACK (please address all points):\n{critic_feedback}\n"
        )
    content_parts.append("Please write the document now.")

    messages: list[dict] = [
        {"role": "user", "content": "\n\n".join(content_parts)}
    ]

    if config.VERBOSE:
        mode = "revision" if critic_feedback else "first draft"
        print(f"\n  [WRITER] Writing {mode}...")

    # The Writer doesn't use tools, so we only need one API call
    # (no agentic loop needed — just one request, one response)
    response = prov.call_api(
        client=client,
        provider=config.PROVIDER,
        model=model,
        max_tokens=config.MAX_TOKENS_PER_AGENT,
        system=WRITER_SYSTEM_PROMPT,
        tools=None,
        messages=messages,
    )

    draft = _extract_text(response.content)
    if config.VERBOSE:
        print(f"  [WRITER] Draft complete. Length: {len(draft)} chars")
    return draft


def _extract_text(content_blocks) -> str:
    return "\n".join(
        getattr(b, "text", b.get("text", ""))
        for b in content_blocks
        if (getattr(b, "type", b.get("type")) == "text")
    ).strip()
