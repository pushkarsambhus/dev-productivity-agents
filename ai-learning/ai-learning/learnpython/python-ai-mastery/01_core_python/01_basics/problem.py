"""
PHASE 1 | CORE PYTHON | 01 BASICS
==================================
Topic: Variables, types, conditionals, loops, functions

Work through each exercise below. Each has a TODO.
Run this file to check your output: python problem.py
"""

# ── Exercise 1: Types & String Formatting ──────────────────────────────────────
# TODO: Create variables for your name (str), years of experience (int),
# and hourly rate (float). Print a sentence using an f-string.
# Expected output: "Pushkar has 16 years of experience at $150.00/hr"

name = None
years = None
rate = None
# print(f"...")


# ── Exercise 2: Conditionals ───────────────────────────────────────────────────
# TODO: Write a function that classifies an engineer's seniority.
# Rules: 0-2 yrs → "junior", 3-5 → "mid", 6-10 → "senior", 11+ → "principal"

def classify_engineer(years_exp: int) -> str:
    pass  # replace with your logic


# ── Exercise 3: Loops ──────────────────────────────────────────────────────────
# TODO: Given a list of build times (in seconds), print only the ones that
# took longer than 60 seconds, and count how many there were.

build_times = [12, 75, 45, 120, 30, 95, 8, 200, 55, 61]

# your loop here


# ── Exercise 4: List Comprehension ────────────────────────────────────────────
# TODO: Using a list comprehension, produce a new list of build times
# that are over 60 seconds, each divided by 60 (converted to minutes).
# Round each to 2 decimal places.

over_threshold = []  # replace with list comprehension


# ── Exercise 5: Functions with defaults ───────────────────────────────────────
# TODO: Write a function `retry(fn, attempts=3, delay=1.0)` that calls fn()
# up to `attempts` times. If fn() raises an exception, catch it, print the
# error, and try again. If all attempts fail, raise the last exception.
# Hint: use a for loop and try/except

def retry(fn, attempts=3, delay=1.0):
    pass


# ── Self-check ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Exercise 2 checks ===")
    print(classify_engineer(1))   # junior
    print(classify_engineer(4))   # mid
    print(classify_engineer(8))   # senior
    print(classify_engineer(16))  # principal

    print("\n=== Exercise 4 check ===")
    print(over_threshold)  # [1.25, 2.0, 1.58, 3.33, 1.02]
