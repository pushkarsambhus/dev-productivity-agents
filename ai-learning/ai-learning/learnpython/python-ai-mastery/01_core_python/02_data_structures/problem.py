"""
PHASE 1 | CORE PYTHON | 02 DATA STRUCTURES
===========================================
Topic: Lists, dicts, sets, tuples — the Python workhorses.
These show up constantly in AI/ML code (token counts, embedding maps, dedup).
"""

# ── Exercise 1: Dict operations ────────────────────────────────────────────────
# You have a list of LLM API calls with their token counts.
# TODO: Build a dict that maps model_name → total_tokens used across all calls.

api_calls = [
    {"model": "claude-3-opus", "tokens": 1200},
    {"model": "claude-3-sonnet", "tokens": 800},
    {"model": "claude-3-opus", "tokens": 950},
    {"model": "gpt-4", "tokens": 1500},
    {"model": "claude-3-sonnet", "tokens": 600},
    {"model": "gpt-4", "tokens": 900},
]

token_totals = {}  # TODO: populate this
# Expected: {'claude-3-opus': 2150, 'claude-3-sonnet': 1400, 'gpt-4': 2400}


# ── Exercise 2: Dict comprehension ────────────────────────────────────────────
# TODO: From token_totals above, create a new dict of only models
# that used more than 2000 tokens total.

heavy_users = {}  # replace with dict comprehension


# ── Exercise 3: Sets for deduplication ────────────────────────────────────────
# In a RAG pipeline, you retrieve document chunk IDs from multiple queries.
# Some chunks appear in multiple query results (retrieved multiple times).
# TODO: Return only unique chunk IDs, sorted.

retrieved = [
    ["chunk_001", "chunk_003", "chunk_007"],
    ["chunk_002", "chunk_003", "chunk_009"],
    ["chunk_007", "chunk_010", "chunk_001"],
]

unique_chunks = []  # TODO: flatten and deduplicate


# ── Exercise 4: Tuples as records ─────────────────────────────────────────────
# TODO: You have eval results as (test_name, passed, latency_ms) tuples.
# Return a list of test names that FAILED (passed=False), sorted alphabetically.

eval_results = [
    ("test_factual_accuracy", True, 340),
    ("test_hallucination", False, 290),
    ("test_refusal_safety", True, 180),
    ("test_context_recall", False, 410),
    ("test_answer_relevance", True, 220),
]

failed_tests = []  # TODO


# ── Exercise 5: defaultdict ────────────────────────────────────────────────────
# TODO: Redo Exercise 1 using collections.defaultdict(int)
# This is the idiomatic Python way — no KeyError handling needed.

from collections import defaultdict

token_totals_v2 = defaultdict(int)
# TODO: populate from api_calls


# ── Self-check ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("token_totals:", token_totals)
    print("heavy_users:", heavy_users)
    print("unique_chunks:", unique_chunks)
    print("failed_tests:", failed_tests)
    print("token_totals_v2:", dict(token_totals_v2))
