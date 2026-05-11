"""
PHASE 1 | CORE PYTHON | 05 PYTHONIC IDIOMS
==========================================
Topic: The patterns that separate "writes Python" from "writes Pythonic Python".
Interviewers at principal level notice these immediately.
"""

# ── Exercise 1: enumerate & zip ───────────────────────────────────────────────
# TODO: Given two lists, print each pair with its index using enumerate + zip.
# Expected:
#   0: chunk_001 → 0.92
#   1: chunk_002 → 0.87
#   2: chunk_003 → 0.71

chunk_ids = ["chunk_001", "chunk_002", "chunk_003"]
scores    = [0.92, 0.87, 0.71]

# your code here (no manual index variable)


# ── Exercise 2: any() / all() ─────────────────────────────────────────────────
# TODO: Write two one-liners using any() and all().
# has_failure: True if any eval score is below 0.7
# all_passing: True if all eval scores are 0.8 or above

eval_scores = [0.95, 0.82, 0.68, 0.91, 0.77]

has_failure = None   # TODO
all_passing = None   # TODO


# ── Exercise 3: dict.get() and setdefault() ───────────────────────────────────
# TODO: Safely look up nested config values without KeyError.
# Use .get() with a default where the key might be missing.

config = {
    "model": "claude-3-sonnet",
    "eval": {
        "threshold": 0.8,
    }
}

model      = None  # TODO: get "model", default "gpt-4"
threshold  = None  # TODO: get config["eval"]["threshold"], default 0.7
max_tokens = None  # TODO: get "max_tokens" key (missing), default 2048


# ── Exercise 4: Unpacking ─────────────────────────────────────────────────────
# Python unpacking is powerful and shows up in AI data pipelines everywhere.

# TODO 4a: Unpack first, *middle, last from this list
pipeline_steps = ["ingest", "chunk", "embed", "index", "retrieve", "generate"]
first = middle = last = None  # TODO: one-liner unpack

# TODO 4b: Swap two variables without a temp variable
a, b = 10, 20
# TODO: swap a and b in one line

# TODO 4c: Unpack a dict's items into separate lists in one line
results = {"accuracy": 0.91, "recall": 0.84, "precision": 0.88}
metrics = values = None  # TODO: use zip(*...) trick


# ── Exercise 5: Generator expression vs list comprehension ────────────────────
# Generators are lazy — they don't compute until needed. Use them for large data.
#
# TODO: Rewrite this as a generator expression (use parentheses, not brackets)
# Then use next() to get just the first match without processing the whole list.

documents = [
    {"id": "d1", "text": "AI safety research", "flagged": False},
    {"id": "d2", "text": "Prompt injection attack", "flagged": True},
    {"id": "d3", "text": "Model evaluation", "flagged": False},
    {"id": "d4", "text": "Jailbreak attempt", "flagged": True},
]

# List comprehension (eager — builds full list even if you only need first):
flagged_list = [d for d in documents if d["flagged"]]

# TODO: Generator version + use next() to get the first flagged doc efficiently
first_flagged = None  # TODO


# ── Self-check ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Ex 2 ===")
    print(f"has_failure: {has_failure}")  # True
    print(f"all_passing: {all_passing}")  # False

    print("\n=== Ex 3 ===")
    print(model, threshold, max_tokens)   # claude-3-sonnet  0.8  2048

    print("\n=== Ex 4a ===")
    print(first, middle, last)            # ingest  [...]  generate

    print("\n=== Ex 4c ===")
    print(metrics)    # ('accuracy', 'recall', 'precision')
    print(values)     # (0.91, 0.84, 0.88)

    print("\n=== Ex 5 ===")
    print(first_flagged)   # {'id': 'd2', ...}
