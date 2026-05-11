"""
config.py — Central configuration for the AI Product Evaluation project.

This module is the single source of truth for all settings: model names, pricing,
SLA thresholds, and experiment parameters. Keeping config in one place lets PMs,
EMs, and TPMs adjust budgets, targets, and model choices without touching logic.
"""

import os

# ---------------------------------------------------------------------------
# API & Models
# ---------------------------------------------------------------------------

ANTHROPIC_API_KEY: str = os.environ.get("ANTHROPIC_API_KEY", "")
OPENAI_API_KEY:    str = os.environ.get("OPENAI_API_KEY", "")

# PROVIDER is set at startup by provider.choose_provider() — do not set manually.
PROVIDER: str = ""   # "anthropic" | "openai"

# Anthropic models:
# Model A: cheap and fast — ideal for high-volume, latency-sensitive tasks
MODEL_A: str = "claude-haiku-4-5-20251001"

# Model B: more capable — use when quality matters more than cost
MODEL_B: str = "claude-sonnet-4-6"

# Judge model: evaluates quality of responses from MODEL_A and MODEL_B
JUDGE_MODEL: str = "claude-sonnet-4-6"

# OpenAI equivalents:
MODEL_A_OPENAI: str = "gpt-4o-mini"   # cheap/fast equivalent
MODEL_B_OPENAI: str = "gpt-4o"        # capable equivalent
JUDGE_MODEL_OPENAI: str = "gpt-4o"

# ---------------------------------------------------------------------------
# Token pricing (USD per million tokens) — update when Anthropic changes prices
# Source: https://www.anthropic.com/pricing
# ---------------------------------------------------------------------------
TOKEN_PRICING: dict[str, dict[str, float]] = {
    # Anthropic
    "claude-haiku-4-5-20251001": {
        "input": 0.80,    # $0.80 per million input tokens
        "output": 4.00,   # $4.00 per million output tokens
    },
    "claude-sonnet-4-6": {
        "input": 3.00,    # $3.00 per million input tokens
        "output": 15.00,  # $15.00 per million output tokens
    },
    # OpenAI (approximate pricing — verify at platform.openai.com/pricing)
    "gpt-4o-mini": {
        "input": 0.15,    # $0.15 per million input tokens
        "output": 0.60,   # $0.60 per million output tokens
    },
    "gpt-4o": {
        "input": 2.50,    # $2.50 per million input tokens
        "output": 10.00,  # $10.00 per million output tokens
    },
}

# ---------------------------------------------------------------------------
# SLA (Service Level Agreement) thresholds
# These are the latency targets your product must meet for a good user experience.
# P50 = median response time; P95 = 95th percentile (tail latency)
# ---------------------------------------------------------------------------
SLA_LATENCY_P50_MS: int = 2000   # 2 seconds median
SLA_LATENCY_P95_MS: int = 5000   # 5 seconds at the 95th percentile

# ---------------------------------------------------------------------------
# Quality thresholds
# LLM-as-judge scores responses 1–10. This is the minimum acceptable score.
# Setting it at 7.0 means we require "good" responses — not just "acceptable".
# ---------------------------------------------------------------------------
MIN_QUALITY_SCORE: float = 7.0

# ---------------------------------------------------------------------------
# A/B experiment configuration
# How many prompts to test per experiment run. More = more confident results,
# but also more API cost. 20 gives reasonable statistical power at low cost.
# ---------------------------------------------------------------------------
EXPERIMENT_SAMPLE_SIZE: int = 20

# ---------------------------------------------------------------------------
# Verbosity — set VERBOSE=1 in environment for debug output
# ---------------------------------------------------------------------------
VERBOSE: bool = os.environ.get("VERBOSE", "0").strip() in ("1", "true", "yes")
