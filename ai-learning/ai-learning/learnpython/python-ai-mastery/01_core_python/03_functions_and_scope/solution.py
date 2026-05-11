"""
SOLUTION: Phase 1 | Core Python | 03 Functions & Scope
"""
import time
from functools import wraps


# ── Exercise 1 ─────────────────────────────────────────────────────────────────
def log_call(fn_name, *args, **kwargs):
    args_str = ", ".join(repr(a) for a in args)
    kwargs_str = ", ".join(f"{k}={v!r}" for k, v in kwargs.items())
    all_args = ", ".join(filter(None, [args_str, kwargs_str]))
    print(f"Calling {fn_name}({all_args})")
    # !r applies repr() — adds quotes around strings, shows types clearly
    # filter(None, [...]) drops empty strings so we don't get a leading comma


# ── Exercise 2 ─────────────────────────────────────────────────────────────────
def timer(fn):
    @wraps(fn)  # preserves fn.__name__, fn.__doc__ — always use this
    def wrapper(*args, **kwargs):
        start = time.perf_counter()      # perf_counter is more precise than time()
        result = fn(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{fn.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

@timer
def slow_embedding(text: str) -> list[float]:
    time.sleep(0.05)
    return [0.1, 0.2, 0.3]


# ── Exercise 3 ─────────────────────────────────────────────────────────────────
def make_prompt_template(system_prompt: str):
    def format_prompt(user_message: str) -> str:
        return f"System: {system_prompt}\nUser: {user_message}"
    return format_prompt
    # format_prompt "closes over" system_prompt — it remembers it even after
    # make_prompt_template has returned. This is a closure.
    # Real use case: LangChain's ChatPromptTemplate works exactly this way.


# ── Exercise 4 ─────────────────────────────────────────────────────────────────
def get_embedding(text: str, cache: dict = None) -> list:
    if cache is None:
        cache = {}                        # fresh dict each call (unless passed in)
    if text not in cache:
        cache[text] = [len(text) * 0.1]
    return cache[text]
    # WHY the bug exists: default args are evaluated ONCE at function definition,
    # not per call. So the {} is created once and shared across all calls.
    # The fix: use None as default, create the object inside the function.


# ── Exercise 5 ─────────────────────────────────────────────────────────────────
eval_results = [
    {"name": "test_refusal", "score": 0.95},
    {"name": "test_recall",  "score": 0.80},
    {"name": "test_accuracy","score": 0.95},
    {"name": "test_latency", "score": 0.60},
    {"name": "test_context", "score": 0.80},
]

sorted_results = sorted(
    eval_results,
    key=lambda r: (-r["score"], r["name"])  # negate score for descending; name for asc tiebreak
)
# Tuple keys: Python sorts tuples element by element.
# Negating a numeric field is the idiomatic way to reverse sort direction
# without using reverse=True (which would also reverse the name sort).


if __name__ == "__main__":
    log_call("embed_text", text="hello world", model="ada-002", truncate=True)
    result = slow_embedding("test input")
    print(f"Result: {result}")
    safety_prompt = make_prompt_template("You are a safe, helpful assistant.")
    print(safety_prompt("Tell me about Paris"))
    print(get_embedding("hello"))
    print(get_embedding("hello"))
    print("\nSorted eval results:")
    for r in sorted_results:
        print(f"  {r['name']}: {r['score']}")
