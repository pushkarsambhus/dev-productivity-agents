"""
PHASE 5 | INTERVIEW PROBLEMS | 01 EASY
=======================================
These are warm-up problems — expect them in screening rounds or as openers
before harder problems. Solve each in < 5 minutes.
"""

# ── 1. FizzBuzz (the classic) ──────────────────────────────────────────────────
# Return a list of strings 1..n:
# Multiples of 3 → "Fizz", multiples of 5 → "Buzz", both → "FizzBuzz"

def fizzbuzz(n: int) -> list[str]:
    pass


# ── 2. Reverse a String ───────────────────────────────────────────────────────
# Without using [::-1] — use two pointers.

def reverse_string(s: str) -> str:
    pass


# ── 3. Count Vowels ───────────────────────────────────────────────────────────
def count_vowels(s: str) -> int:
    pass


# ── 4. Is Palindrome ──────────────────────────────────────────────────────────
# Ignore spaces and case. "A man a plan a canal Panama" → True

def is_palindrome(s: str) -> bool:
    pass


# ── 5. Find Duplicates ────────────────────────────────────────────────────────
# Return list of elements that appear more than once, in order of first duplicate.

def find_duplicates(items: list) -> list:
    pass


# ── 6. Flatten Nested List ────────────────────────────────────────────────────
# Flatten one level deep: [[1,2],[3,[4,5]],6] → [1,2,3,[4,5],6]

def flatten_one_level(nested: list) -> list:
    pass


# ── 7. Running Average ────────────────────────────────────────────────────────
# Given a list of numbers, return a list of running averages.
# [1, 2, 3, 4] → [1.0, 1.5, 2.0, 2.5]

def running_average(nums: list[float]) -> list[float]:
    pass


# ── 8. Most Common Element ────────────────────────────────────────────────────
# Return the element that appears most often. Ties: return any.

def most_common(items: list):
    pass


# ── Self-check ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(fizzbuzz(15))
    # ['1','2','Fizz','4','Buzz','Fizz','7','8','Fizz','Buzz','11','Fizz','13','14','FizzBuzz']

    print(reverse_string("hello"))          # "olleh"
    print(count_vowels("hello world"))      # 3
    print(is_palindrome("A man a plan a canal Panama"))  # True
    print(find_duplicates([1,2,3,2,4,1,5])) # [2, 1]
    print(flatten_one_level([[1,2],[3,[4,5]],6]))  # [1,2,3,[4,5],6]
    print(running_average([1,2,3,4]))       # [1.0, 1.5, 2.0, 2.5]
    print(most_common([1,2,2,3,3,3,1]))     # 3
