"""
config.py — Configuration for the multi-agent system.

LEARNING NOTE — What changes in multi-agent systems:
    Single agent: one Claude conversation, one tool loop.
    Multi-agent:  multiple Claude conversations, each with its own role,
                  tools, and potentially different models.

    Key design decisions:
      1. Which model should each agent use?
         Expensive models for reasoning-heavy tasks (orchestrator, critic).
         Cheap models for simple tasks (summarizer, formatter).
      2. Should agents share a conversation history or have their own?
         Shared  → agents know what other agents said (more context, more tokens)
         Isolated → agents only see their own task (cheaper, less confusion)
      3. How does the orchestrator communicate results between agents?
         This file lets you tune all of that.
"""

import os

# ─────────────────────────────────────────────────────────────────────────────
# 🔑  API KEY  ← YOU MUST FILL THIS IN
# ─────────────────────────────────────────────────────────────────────────────
ANTHROPIC_API_KEY: str = os.environ.get("ANTHROPIC_API_KEY", "")
OPENAI_API_KEY:    str = os.environ.get("OPENAI_API_KEY", "")

# PROVIDER is set at startup by provider.choose_provider() — do not set manually.
PROVIDER: str = ""   # "anthropic" | "openai"

# ─────────────────────────────────────────────────────────────────────────────
# 🤖  PER-AGENT MODELS
# ─────────────────────────────────────────────────────────────────────────────
# TRADE-OFF: using different models per agent balances cost and quality.
#   • Orchestrator needs the most reasoning → most capable model
#   • Worker agents can often use cheaper models
#   • Using the same model everywhere is simpler but costs more

# Main orchestrator — decides the plan and synthesises the final answer
ORCHESTRATOR_MODEL: str = "claude-opus-4-6"
ORCHESTRATOR_MODEL_OPENAI: str = "gpt-4o"

# Researcher — retrieves and summarises facts
RESEARCHER_MODEL: str = "claude-opus-4-6"
RESEARCHER_MODEL_OPENAI: str = "gpt-4o"

# Writer — turns facts into readable prose
WRITER_MODEL: str = "claude-opus-4-6"
WRITER_MODEL_OPENAI: str = "gpt-4o"

# Critic — reviews and improves the draft
CRITIC_MODEL: str = "claude-opus-4-6"
CRITIC_MODEL_OPENAI: str = "gpt-4o"

# ─────────────────────────────────────────────────────────────────────────────
# 🛑  SAFETY LIMITS
# ─────────────────────────────────────────────────────────────────────────────
MAX_TURNS_PER_AGENT: int = 8     # each sub-agent gets this many tool-call rounds
MAX_TOKENS_PER_AGENT: int = 2048 # max output per API call
MAX_REVISION_ROUNDS: int = 2     # how many Critic → Writer loops to allow

# ─────────────────────────────────────────────────────────────────────────────
# 🌐  EXTERNAL API KEYS
# ─────────────────────────────────────────────────────────────────────────────
SEARCH_API_KEY: str = os.environ.get("SEARCH_API_KEY", "")
# TODO: add your search API key for real web search

# ─────────────────────────────────────────────────────────────────────────────
# 🔍  DEBUG FLAGS
# ─────────────────────────────────────────────────────────────────────────────
VERBOSE: bool = True   # show each agent's actions
SHOW_AGENT_THOUGHTS: bool = True  # show reasoning text from each agent
