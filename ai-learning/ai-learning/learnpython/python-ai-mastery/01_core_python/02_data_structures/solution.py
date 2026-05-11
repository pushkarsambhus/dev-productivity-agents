"""
SOLUTION: Phase 1 | Core Python | 02 Data Structures
"""
from collections import defaultdict

api_calls = [
    {"model": "claude-3-opus", "tokens": 1200},
    {"model": "claude-3-sonnet", "tokens": 800},
    {"model": "claude-3-opus", "tokens": 950},
    {"model": "gpt-4", "tokens": 1500},
    {"model": "claude-3-sonnet", "tokens": 600},
    {"model": "gpt-4", "tokens": 900},
]

# ── Exercise 1 ─────────────────────────────────────────────────────────────────
token_totals = {}
for call in api_calls:
    model = call["model"]
    token_totals[model] = token_totals.get(model, 0) + call["tokens"]
# .get(key, default) is safer than [] — no KeyError if key is new


# ── Exercise 2 ─────────────────────────────────────────────────────────────────
heavy_users = {model: tokens for model, tokens in token_totals.items() if tokens > 2000}
# Dict comprehension: {key_expr: val_expr for k, v in dict.items() if condition}


# ── Exercise 3 ─────────────────────────────────────────────────────────────────
retrieved = [
    ["chunk_001", "chunk_003", "chunk_007"],
    ["chunk_002", "chunk_003", "chunk_009"],
    ["chunk_007", "chunk_010", "chunk_001"],
]
# Flatten with a nested comprehension, then convert to set, then sort
unique_chunks = sorted(set(chunk for sublist in retrieved for chunk in sublist))
# Read as: "for each sublist in retrieved, for each chunk in sublist"
# This double-loop comprehension pattern is very common in data processing


# ── Exercise 4 ─────────────────────────────────────────────────────────────────
eval_results = [
    ("test_factual_accuracy", True, 340),
    ("test_hallucination", False, 290),
    ("test_refusal_safety", True, 180),
    ("test_context_recall", False, 410),
    ("test_answer_relevance", True, 220),
]
failed_tests = sorted(name for name, passed, _ in eval_results if not passed)
# Tuple unpacking in comprehension: (name, passed, _) — _ signals "don't care"


# ── Exercise 5 ─────────────────────────────────────────────────────────────────
token_totals_v2 = defaultdict(int)
for call in api_calls:
    token_totals_v2[call["model"]] += call["tokens"]
# defaultdict(int) initializes missing keys to 0 automatically
# Much cleaner than .get() for accumulation patterns


if __name__ == "__main__":
    print("token_totals:", token_totals)
    print("heavy_users:", heavy_users)
    print("unique_chunks:", unique_chunks)
    print("failed_tests:", failed_tests)
    print("token_totals_v2:", dict(token_totals_v2))
