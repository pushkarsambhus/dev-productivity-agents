"""
config.py — Central configuration for the single agent.

LEARNING NOTE:
    Centralizing config makes it easy to swap models, tune parameters,
    and understand ALL the knobs in one place before you start reading
    the agent loop code.

TRADE-OFFS:
    - Hardcoding defaults here is fast but inflexible. In production you'd
      load from environment variables or a YAML/TOML file so each deployment
      can differ without touching code.
    - Keeping config in one module avoids magic constants scattered across files.
"""

import os

# ─────────────────────────────────────────────
# 🔑  API KEY  ← YOU MUST FILL THIS IN
# ─────────────────────────────────────────────
# Option A (recommended): set the environment variable before running
#   export ANTHROPIC_API_KEY="sk-ant-..."
# Option B: hard-code it here (never commit this to git!)
ANTHROPIC_API_KEY: str = os.environ.get("ANTHROPIC_API_KEY", "")
OPENAI_API_KEY:    str = os.environ.get("OPENAI_API_KEY", "")

# PROVIDER is set at startup by provider.choose_provider() — do not set manually.
PROVIDER: str = ""   # "anthropic" | "openai"

# ─────────────────────────────────────────────
# 🤖  MODEL SELECTION
# ─────────────────────────────────────────────
# Anthropic: claude-opus-4-6    → most capable, highest cost
#            claude-sonnet-4-6  → balanced speed / capability
#            claude-haiku-4-5   → fastest, cheapest
MODEL: str = "claude-opus-4-6"

# OpenAI equivalents:
#   gpt-4o       → comparable to claude-opus (most capable)
#   gpt-4o-mini  → comparable to claude-haiku (fast / cheap)
MODEL_OPENAI: str = "gpt-4o"

# ─────────────────────────────────────────────
# 🛑  SAFETY LIMITS
# ─────────────────────────────────────────────
# TRADE-OFF: too low → agent can't finish complex tasks
#            too high → runaway loops burn API credits
MAX_TURNS: int = 10          # max tool-call rounds before we force-stop
MAX_TOKENS: int = 4096       # max output tokens per API call

# ─────────────────────────────────────────────
# 🧠  AGENT BEHAVIOUR
# ─────────────────────────────────────────────
# System prompt = the agent's "personality" and instructions.
# TRADE-OFF: very long system prompts cost tokens on every call.
#            Keep stable text here; inject dynamic context per-request.
SYSTEM_PROMPT: str = """You are a helpful research assistant.

You have access to the following tools:
- web_search: search the internet for information
- calculator: perform arithmetic and math operations
- get_current_time: get today's date and time
- fetch_url: fetch the text content of a URL

RULES:
1. Always reason step-by-step before choosing a tool.
2. If a tool call fails, report the error and try an alternative approach.
3. When you have enough information, give a clear final answer.
4. Cite your sources when using web_search results.
"""

# ─────────────────────────────────────────────
# 🌐  EXTERNAL API KEYS  ← YOU FILL THESE IN
# ─────────────────────────────────────────────
# The web_search tool below calls a real search API.
# Sign up for a free key at https://serpapi.com  or  https://serper.dev
# TODO: add your search API key
SEARCH_API_KEY: str = os.environ.get("SEARCH_API_KEY", "")
SEARCH_API_PROVIDER: str = "serper"   # "serpapi" | "serper" | "brave"
# TODO: if you change SEARCH_API_PROVIDER, update _call_search_api() in tools.py

# Logging — set to True while learning to see every API call
VERBOSE: bool = True
