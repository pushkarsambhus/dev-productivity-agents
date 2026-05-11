"""
SOLUTION: Phase 1 | Core Python | 01 Basics
"""

# ── Exercise 1 ─────────────────────────────────────────────────────────────────
name = "Pushkar"
years = 16
rate = 150.0
print(f"{name} has {years} years of experience at ${rate:.2f}/hr")


# ── Exercise 2 ─────────────────────────────────────────────────────────────────
def classify_engineer(years_exp: int) -> str:
    # Key interview idiom: early returns, no else-after-return (Pylint R1705)
    if years_exp <= 2:
        return "junior"
    if years_exp <= 5:
        return "mid"
    if years_exp <= 10:
        return "senior"
    return "principal"
    # WHY no else: once you return, the else branch is unreachable — it's noise.


# ── Exercise 3 ─────────────────────────────────────────────────────────────────
build_times = [12, 75, 45, 120, 30, 95, 8, 200, 55, 61]
slow_count = 0
for t in build_times:
    if t > 60:
        print(f"  Slow build: {t}s")
        slow_count += 1
print(f"Total slow builds: {slow_count}")


# ── Exercise 4 ─────────────────────────────────────────────────────────────────
over_threshold = [round(t / 60, 2) for t in build_times if t > 60]
# Pattern: [expression for item in iterable if condition]
# This is one of the most common Python idioms — learn to read and write it fast.


# ── Exercise 5 ─────────────────────────────────────────────────────────────────
import time

def retry(fn, attempts=3, delay=1.0):
    last_exception = None
    for attempt in range(1, attempts + 1):
        try:
            return fn()           # if it succeeds, return immediately
        except Exception as e:
            last_exception = e
            print(f"Attempt {attempt} failed: {e}")
            if attempt < attempts:
                time.sleep(delay)
    raise last_exception          # all attempts exhausted
    # WHY save last_exception: we want to re-raise the actual error, not a generic one.
    # This pattern appears in production retry decorators and AI pipeline error handling.


# ── Self-check ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n=== Exercise 2 checks ===")
    print(classify_engineer(1))   # junior
    print(classify_engineer(4))   # mid
    print(classify_engineer(8))   # senior
    print(classify_engineer(16))  # principal

    print("\n=== Exercise 4 check ===")
    print(over_threshold)         # [1.25, 2.0, 1.58, 3.33, 1.02]
