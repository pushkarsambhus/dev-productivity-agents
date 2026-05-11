"""
tools.py — Tool definitions for the single agent.

LEARNING NOTE — What is a "tool"?
    A tool is a function your agent can call to interact with the outside world.
    Claude doesn't run code — it emits a JSON object asking YOU to run a function.
    Your harness (agent.py) reads that JSON, calls the matching function, and
    sends the result back so Claude can continue reasoning.

    Every tool has three parts:
      1. Schema  – tells Claude what the tool is called, what it does, and what
                   parameters it accepts (JSON Schema format).
      2. Handler – the Python function that actually does the work.
      3. Registry – maps tool names → handler functions so agent.py can dispatch.

TRADE-OFFS:
    - More tools  → Claude has more power but the prompt gets longer (costs tokens)
                    and Claude may pick the wrong tool if descriptions are vague.
    - Fewer tools → simpler, cheaper, but the agent can't do as much.
    - Real APIs   → useful results but add latency and external dependencies.
    - Simulated   → great for testing/learning without spending on API credits.
"""

import json
import math
import datetime
from typing import Any
import config

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1: TOOL SCHEMAS
# These are the descriptions Claude reads to decide WHEN and HOW to call tools.
# Clear descriptions → correct tool selection.
# ─────────────────────────────────────────────────────────────────────────────

TOOL_SCHEMAS: list[dict] = [
    {
        "name": "web_search",
        "description": (
            "Search the internet for current information. "
            "Use this when you need facts, news, or data you don't already know. "
            "Returns a list of relevant results with titles, snippets, and URLs."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query. Be specific for better results.",
                },
                "num_results": {
                    "type": "integer",
                    "description": "How many results to return (1-10). Default 5.",
                    "default": 5,
                },
            },
            "required": ["query"],
        },
    },
    {
        "name": "calculator",
        "description": (
            "Evaluate a mathematical expression and return the numeric result. "
            "Supports +, -, *, /, **, sqrt, sin, cos, log, and standard Python math. "
            "Always use this instead of guessing arithmetic."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "A Python math expression, e.g. '2 ** 10' or 'math.sqrt(144)'.",
                },
            },
            "required": ["expression"],
        },
    },
    {
        "name": "get_current_time",
        "description": "Return the current date, time, and UTC offset. Use before any time-sensitive task.",
        "input_schema": {
            "type": "object",
            "properties": {
                "timezone": {
                    "type": "string",
                    "description": "IANA timezone string, e.g. 'America/New_York'. Defaults to UTC.",
                    "default": "UTC",
                },
            },
            "required": [],
        },
    },
    {
        "name": "fetch_url",
        "description": (
            "Fetch the text content of a web page given its URL. "
            "Use this to read articles, documentation, or any specific page. "
            "Returns plain text (HTML stripped)."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The full URL to fetch, including https://",
                },
                "max_chars": {
                    "type": "integer",
                    "description": "Truncate response to this many characters. Default 3000.",
                    "default": 3000,
                },
            },
            "required": ["url"],
        },
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2: TOOL HANDLERS
# Each function matches a schema above.  Return a plain string — Claude reads it.
# ─────────────────────────────────────────────────────────────────────────────


def handle_web_search(query: str, num_results: int = 5) -> str:
    """
    Call a real search API and return formatted results.

    TODO: The real implementation requires a search API key (see config.py).
          Until you add one, a simulated response is returned so you can
          learn the agent loop without spending money.
    """

    # ── REAL IMPLEMENTATION (uncomment after adding your API key) ────────────
    # return _call_search_api(query, num_results)
    # ─────────────────────────────────────────────────────────────────────────

    # ── SIMULATED RESPONSE (used when no key is set) ─────────────────────────
    # LEARNING NOTE: This lets you run the agent offline.
    # Replace with the real call above once you have your key.
    if not config.SEARCH_API_KEY:
        return _simulated_search(query, num_results)

    return _call_search_api(query, num_results)


def _call_search_api(query: str, num_results: int) -> str:
    """
    Real search call.  Supports Serper (default), SerpAPI, or Brave.

    TODO: Select your provider in config.py and add your key.
    """
    import urllib.request

    if config.SEARCH_API_PROVIDER == "serper":
        # Serper.dev — https://serper.dev (free tier available)
        url = "https://google.serper.dev/search"
        payload = json.dumps({"q": query, "num": num_results}).encode()
        req = urllib.request.Request(
            url,
            data=payload,
            headers={
                "X-API-KEY": config.SEARCH_API_KEY,
                "Content-Type": "application/json",
            },
        )
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
        results = data.get("organic", [])
        lines = []
        for r in results[:num_results]:
            lines.append(f"Title: {r.get('title')}")
            lines.append(f"URL: {r.get('link')}")
            lines.append(f"Snippet: {r.get('snippet')}\n")
        return "\n".join(lines) if lines else "No results found."

    # TODO: add elif branches for other providers (serpapi, brave)
    return "Search provider not configured. See config.py."


def _simulated_search(query: str, num_results: int) -> str:
    """Offline placeholder — teaches the loop without real API calls."""
    return (
        f"[SIMULATED SEARCH for '{query}']\n\n"
        "Result 1: Example article about your query\n"
        "URL: https://example.com/article\n"
        "Snippet: This is where real search results would appear once you "
        "add a SEARCH_API_KEY to config.py.\n\n"
        "To enable real search:\n"
        "  1. Get a free key at https://serper.dev\n"
        "  2. Set SEARCH_API_KEY in config.py or as an env variable.\n"
    )


def handle_calculator(expression: str) -> str:
    """
    Safely evaluate a math expression.

    SECURITY NOTE: Never use eval() on untrusted input in production.
    Here we restrict the allowed namespace to math functions only.
    TRADE-OFF: restricting namespace prevents arbitrary code execution
               but limits what expressions can be used.
    """
    # Build a safe namespace: only math functions + builtins
    safe_namespace: dict[str, Any] = {
        "math": math,
        "sqrt": math.sqrt,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "log": math.log,
        "log10": math.log10,
        "exp": math.exp,
        "pi": math.pi,
        "e": math.e,
        "abs": abs,
        "round": round,
        "pow": pow,
        "__builtins__": {},   # ← block all other builtins
    }
    try:
        result = eval(expression, safe_namespace)  # noqa: S307
        return f"Result: {result}"
    except Exception as exc:
        return f"Calculator error: {exc}"


def handle_get_current_time(timezone: str = "UTC") -> str:
    """
    Return current time.  timezone parameter is accepted but we use UTC
    unless you add the 'pytz' package.

    TODO: pip install pytz and uncomment the timezone conversion below
          for accurate local-time support.
    """
    now_utc = datetime.datetime.utcnow()

    # ── REAL TIMEZONE SUPPORT (requires: pip install pytz) ───────────────────
    # import pytz
    # try:
    #     tz = pytz.timezone(timezone)
    #     now = datetime.datetime.now(tz)
    #     return f"Current time ({timezone}): {now.strftime('%Y-%m-%d %H:%M:%S %Z%z')}"
    # except pytz.UnknownTimeZoneError:
    #     return f"Unknown timezone: {timezone}. Falling back to UTC."
    # ─────────────────────────────────────────────────────────────────────────

    return (
        f"Current UTC time: {now_utc.strftime('%Y-%m-%d %H:%M:%S')} UTC\n"
        f"(Requested timezone: {timezone} — install pytz for local time support)"
    )


def handle_fetch_url(url: str, max_chars: int = 3000) -> str:
    """
    Fetch a URL and return plain text content.

    SECURITY NOTE: In production, validate/whitelist URLs and add
    timeouts to prevent SSRF and hanging requests.

    TODO: For JavaScript-rendered pages (SPAs) use playwright or selenium.
    """
    import urllib.request
    import html.parser

    class _HTMLStripper(html.parser.HTMLParser):
        """Minimal HTML → plain-text converter."""
        def __init__(self):
            super().__init__()
            self.text_parts: list[str] = []
            self._skip = False

        def handle_starttag(self, tag, attrs):
            if tag in {"script", "style", "nav", "footer"}:
                self._skip = True

        def handle_endtag(self, tag):
            if tag in {"script", "style", "nav", "footer"}:
                self._skip = False

        def handle_data(self, data):
            if not self._skip and data.strip():
                self.text_parts.append(data.strip())

        def get_text(self) -> str:
            return " ".join(self.text_parts)

    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (agent-learning-bot/1.0)"},
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            raw_html = resp.read().decode("utf-8", errors="replace")

        stripper = _HTMLStripper()
        stripper.feed(raw_html)
        text = stripper.get_text()[:max_chars]
        return f"[Content from {url}]\n\n{text}"

    except Exception as exc:
        return f"Failed to fetch {url}: {exc}"


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3: TOOL REGISTRY
# Maps tool name → handler so agent.py can dispatch with one line.
# ─────────────────────────────────────────────────────────────────────────────

TOOL_REGISTRY: dict[str, Any] = {
    "web_search": lambda args: handle_web_search(**args),
    "calculator": lambda args: handle_calculator(**args),
    "get_current_time": lambda args: handle_get_current_time(**args),
    "fetch_url": lambda args: handle_fetch_url(**args),
}


def dispatch_tool(name: str, tool_input: dict) -> str:
    """
    Execute a tool by name and return the result as a string.

    This is the function agent.py calls when Claude emits a tool_use block.

    LEARNING NOTE: Claude always sends tool_use blocks with:
        {
          "id": "toolu_...",
          "name": "tool_name",
          "input": { ...arguments... }
        }
    We look up the name in TOOL_REGISTRY and pass the input dict.
    """
    handler = TOOL_REGISTRY.get(name)
    if handler is None:
        return f"ERROR: Unknown tool '{name}'. Available tools: {list(TOOL_REGISTRY.keys())}"

    if config.VERBOSE:
        print(f"  [TOOL] {name}({json.dumps(tool_input, ensure_ascii=False)[:120]})")

    try:
        result = handler(tool_input)
        if config.VERBOSE:
            print(f"  [TOOL RESULT] {str(result)[:200]}")
        return result
    except Exception as exc:
        error_msg = f"Tool '{name}' raised an exception: {exc}"
        if config.VERBOSE:
            print(f"  [TOOL ERROR] {error_msg}")
        return error_msg
