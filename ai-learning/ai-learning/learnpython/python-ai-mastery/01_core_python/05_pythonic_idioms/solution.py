"""
SOLUTION: Phase 1 | Core Python | 05 Pythonic Idioms
"""

# ── Exercise 1 ─────────────────────────────────────────────────────────────────
chunk_ids = ["chunk_001", "chunk_002", "chunk_003"]
scores    = [0.92, 0.87, 0.71]

for i, (chunk, score) in enumerate(zip(chunk_ids, scores)):
    print(f"  {i}: {chunk} → {score}")
# zip() pairs elements from two iterables
# enumerate() adds an index
# Tuple unpacking in the for: (chunk, score) unpacks each zip pair


# ── Exercise 2 ─────────────────────────────────────────────────────────────────
eval_scores = [0.95, 0.82, 0.68, 0.91, 0.77]

has_failure = any(s < 0.7 for s in eval_scores)   # True — 0.68 < 0.7
all_passing = all(s >= 0.8 for s in eval_scores)   # False — 0.77 < 0.8
# any/all with generator expressions: lazy, short-circuit on first match


# ── Exercise 3 ─────────────────────────────────────────────────────────────────
config = {"model": "claude-3-sonnet", "eval": {"threshold": 0.8}}

model      = config.get("model", "gpt-4")
threshold  = config.get("eval", {}).get("threshold", 0.7)   # chained .get() for nesting
max_tokens = config.get("max_tokens", 2048)
# .get(key, default) never raises KeyError
# Chaining: config.get("eval", {}) returns {} if "eval" missing, then .get() on that


# ── Exercise 4 ─────────────────────────────────────────────────────────────────
pipeline_steps = ["ingest", "chunk", "embed", "index", "retrieve", "generate"]
first, *middle, last = pipeline_steps
# * collects everything in between into a list

a, b = 10, 20
a, b = b, a   # Python evaluates right side first, then assigns — no temp needed

results = {"accuracy": 0.91, "recall": 0.84, "precision": 0.88}
metrics, values = zip(*results.items())
# results.items() → [("accuracy",0.91), ("recall",0.84), ("precision",0.88)]
# zip(*...) "unzips" — transposes rows to columns
# → metrics=("accuracy","recall","precision"), values=(0.91,0.84,0.88)


# ── Exercise 5 ─────────────────────────────────────────────────────────────────
documents = [
    {"id": "d1", "text": "AI safety research", "flagged": False},
    {"id": "d2", "text": "Prompt injection attack", "flagged": True},
    {"id": "d3", "text": "Model evaluation", "flagged": False},
    {"id": "d4", "text": "Jailbreak attempt", "flagged": True},
]

first_flagged = next((d for d in documents if d["flagged"]), None)
# next(generator, default) — gets first item or returns default if exhausted
# Generator is lazy: stops after finding d2, never processes d3/d4
# This matters at scale: imagine 10M documents — list comp would load all of them


if __name__ == "__main__":
    print("=== Ex 2 ===")
    print(f"has_failure: {has_failure}")
    print(f"all_passing: {all_passing}")
    print("\n=== Ex 3 ===")
    print(model, threshold, max_tokens)
    print("\n=== Ex 4a ===")
    print(first, middle, last)
    print("\n=== Ex 4c ===")
    print(metrics)
    print(values)
    print("\n=== Ex 5 ===")
    print(first_flagged)
