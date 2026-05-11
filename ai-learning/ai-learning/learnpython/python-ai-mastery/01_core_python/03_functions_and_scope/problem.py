"""
PHASE 1 | CORE PYTHON | 03 FUNCTIONS & SCOPE
=============================================
Topic: Closures, decorators, *args/**kwargs, lambda, scope rules.
These patterns appear constantly in AI framework code (LangChain, FastAPI).
"""

# ── Exercise 1: *args and **kwargs ────────────────────────────────────────────
# TODO: Write a function `log_call(fn_name, *args, **kwargs)` that prints
# a formatted log line like:
#   Calling embed_text(text='hello world', model='ada-002', truncate=True)

def log_call(fn_name, *args, **kwargs):
    pass

# Expected:
# log_call("embed_text", text="hello world", model="ada-002", truncate=True)
# → Calling embed_text(text='hello world', model='ada-002', truncate=True)


# ── Exercise 2: Decorator ─────────────────────────────────────────────────────
# Decorators are used everywhere: FastAPI routes, retry logic, timing, caching.
# TODO: Write a decorator `@timer` that prints how long a function took to run.
# Output: "embed_documents took 0.0023s"

import time
from functools import wraps

def timer(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        pass  # TODO: record start, call fn, record end, print elapsed, return result
    return wrapper

@timer
def slow_embedding(text: str) -> list[float]:
    time.sleep(0.05)  # simulates an API call
    return [0.1, 0.2, 0.3]


# ── Exercise 3: Closure ───────────────────────────────────────────────────────
# A closure "remembers" variables from its enclosing scope.
# Used in: prompt template factories, config-bound functions.
#
# TODO: Write a function `make_prompt_template(system_prompt: str)`
# that returns a function. The returned function takes a `user_message`
# and returns the full formatted prompt string.

def make_prompt_template(system_prompt: str):
    pass  # return a function that closes over system_prompt

# Usage:
# safety_prompt = make_prompt_template("You are a safe, helpful assistant.")
# print(safety_prompt("Tell me about Paris"))
# → "System: You are a safe, helpful assistant.\nUser: Tell me about Paris"


# ── Exercise 4: Mutable default argument trap ─────────────────────────────────
# This is a classic Python gotcha that trips up everyone.
# TODO: Fix this buggy function. The bug: the cache dict is shared across calls.

def get_embedding_BAD(text: str, cache: dict = {}) -> list:
    if text not in cache:
        cache[text] = [len(text) * 0.1]  # fake embedding
    return cache[text]

# Fix it:
def get_embedding(text: str, cache: dict = None) -> list:
    pass  # TODO: handle cache=None correctly, then same logic


# ── Exercise 5: Lambda + sorted ───────────────────────────────────────────────
# TODO: Sort these eval results by score descending, then by name ascending
# when scores are tied.

eval_results = [
    {"name": "test_refusal", "score": 0.95},
    {"name": "test_recall",  "score": 0.80},
    {"name": "test_accuracy","score": 0.95},
    {"name": "test_latency", "score": 0.60},
    {"name": "test_context", "score": 0.80},
]

sorted_results = []  # TODO: one-liner using sorted() with a lambda key


# ── Self-check ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    log_call("embed_text", text="hello world", model="ada-002", truncate=True)

    result = slow_embedding("test input")
    print(f"Result: {result}")

    safety_prompt = make_prompt_template("You are a safe, helpful assistant.")
    print(safety_prompt("Tell me about Paris"))

    print(get_embedding("hello"))
    print(get_embedding("hello"))  # should use cache

    print("\nSorted eval results:")
    for r in sorted_results:
        print(f"  {r['name']}: {r['score']}")
