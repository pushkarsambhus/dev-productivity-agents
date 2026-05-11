"""
agents/researcher.py — The Researcher sub-agent.

ROLE: Given a topic or question, gather relevant facts and data.

LEARNING NOTE:
    This is a self-contained agent — it has its own:
      • System prompt (tells it to focus on research, not writing)
      • Tool set     (web_search, fetch_url — the info-gathering tools)
      • Run method   (its own tool-use loop)

    It does NOT have access to the calculator or critic tools.
    TRADE-OFF: narrower tool set → less confusion, lower token cost,
               but the agent can't do things outside its scope.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import json
import math
import datetime
from typing import Optional
import provider as prov
import config


# ─────────────────────────────────────────────────────────────────────────────
# Researcher-specific system prompt
# ─────────────────────────────────────────────────────────────────────────────

RESEARCHER_SYSTEM_PROMPT = """You are a meticulous research specialist.

Your job is to gather factual information about a given topic and return a
structured research report.

PROCESS:
1. Break the topic into specific questions you need to answer.
2. Use web_search to find current information.
3. Use fetch_url to read promising articles for more detail.
4. Compile your findings into a clear research brief with:
   - Key facts
   - Relevant statistics (if any)
   - Important caveats or uncertainties
   - Sources (URL where you found each fact)

Be factual, precise, and cite your sources. Do NOT write in essay form —
a structured list of findings with sources is preferred.
"""


# ─────────────────────────────────────────────────────────────────────────────
# Tools available to the Researcher
# ─────────────────────────────────────────────────────────────────────────────

RESEARCHER_TOOLS = [
    {
        "name": "web_search",
        "description": "Search the internet for current information on a topic.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The search query"},
                "num_results": {"type": "integer", "default": 5},
            },
            "required": ["query"],
        },
    },
    {
        "name": "fetch_url",
        "description": "Fetch the content of a specific web page.",
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "The URL to fetch"},
                "max_chars": {"type": "integer", "default": 3000},
            },
            "required": ["url"],
        },
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# Tool handlers (copied from single-agent project for self-containment)
# In a real system you'd import these from a shared module.
# ─────────────────────────────────────────────────────────────────────────────

def _web_search(query: str, num_results: int = 5) -> str:
    if not config.SEARCH_API_KEY:
        return (
            f"[SIMULATED SEARCH: '{query}']\n"
            "Add SEARCH_API_KEY to config.py for real results.\n"
            "Simulated finding: This is an example research result."
        )
    # TODO: implement real search (see 01-single-agent/tools.py for pattern)
    return f"[SEARCH: '{query}'] No real API key configured."


def _fetch_url(url: str, max_chars: int = 3000) -> str:
    import urllib.request
    import html.parser

    class Stripper(html.parser.HTMLParser):
        def __init__(self):
            super().__init__()
            self.parts = []
            self._skip = False
        def handle_starttag(self, tag, attrs):
            if tag in {"script", "style"}:
                self._skip = True
        def handle_endtag(self, tag):
            if tag in {"script", "style"}:
                self._skip = False
        def handle_data(self, data):
            if not self._skip and data.strip():
                self.parts.append(data.strip())

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
        s = Stripper()
        s.feed(raw)
        return " ".join(s.parts)[:max_chars]
    except Exception as exc:
        return f"Failed to fetch {url}: {exc}"


TOOL_HANDLERS = {
    "web_search": lambda args: _web_search(**args),
    "fetch_url": lambda args: _fetch_url(**args),
}


# ─────────────────────────────────────────────────────────────────────────────
# Main researcher function
# ─────────────────────────────────────────────────────────────────────────────

def run_researcher(topic: str, context: Optional[str] = None) -> str:
    """
    Research a topic and return a structured findings brief.

    Parameters
    ----------
    topic : str
        The research question or topic.
    context : str, optional
        Additional context from the orchestrator (e.g., the user's original
        question, desired depth of research).

    Returns
    -------
    str
        A structured research brief.
    """
    api_key = config.ANTHROPIC_API_KEY if config.PROVIDER == "anthropic" else config.OPENAI_API_KEY
    model   = config.RESEARCHER_MODEL if config.PROVIDER == "anthropic" else config.RESEARCHER_MODEL_OPENAI
    client  = prov.create_client(config.PROVIDER, api_key)

    # Build the initial message — optionally include orchestrator context
    user_content = f"Research topic: {topic}"
    if context:
        user_content += f"\n\nContext from orchestrator:\n{context}"

    messages: list[dict] = [{"role": "user", "content": user_content}]

    if config.VERBOSE:
        print(f"\n  [RESEARCHER] Starting research: '{topic[:80]}'")

    for turn in range(config.MAX_TURNS_PER_AGENT):
        response = prov.call_api(
            client=client,
            provider=config.PROVIDER,
            model=model,
            max_tokens=config.MAX_TOKENS_PER_AGENT,
            system=RESEARCHER_SYSTEM_PROMPT,
            tools=RESEARCHER_TOOLS,
            messages=messages,
        )
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            # Extract the text report
            report = _extract_text(response.content)
            if config.VERBOSE:
                print(f"  [RESEARCHER] Done. Report length: {len(report)} chars")
            return report

        if response.stop_reason == "tool_use":
            results = _execute_tools(response.content)
            messages.append({"role": "user", "content": results})
            continue

    return "[Researcher: max turns reached without completing research]"


def _extract_text(content_blocks) -> str:
    return "\n".join(
        getattr(b, "text", b.get("text", ""))
        for b in content_blocks
        if (getattr(b, "type", b.get("type")) == "text")
    ).strip()


def _execute_tools(content_blocks) -> list[dict]:
    results = []
    for b in content_blocks:
        if getattr(b, "type", b.get("type")) != "tool_use":
            continue
        name  = getattr(b, "name",  b.get("name",  ""))
        tid   = getattr(b, "id",    b.get("id",    ""))
        tinput = getattr(b, "input", b.get("input", {}))
        if config.VERBOSE:
            print(f"    [RESEARCHER TOOL] {name}({json.dumps(tinput)[:80]})")
        handler = TOOL_HANDLERS.get(name)
        result = handler(tinput) if handler else f"Unknown tool: {name}"
        results.append({"type": "tool_result", "tool_use_id": tid, "content": result})
    return results
