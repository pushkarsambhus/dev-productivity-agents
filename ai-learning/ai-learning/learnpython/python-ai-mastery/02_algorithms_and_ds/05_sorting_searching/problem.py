"""
PHASE 2 | ALGORITHMS & DS | 05 SORTING & SEARCHING
===================================================
Topic: Binary search, merge sort, and Python's built-in sort.
Binary search is the most commonly tested "searching" pattern at interviews.
Knowing merge sort shows you understand divide-and-conquer.
"""

# ── Problem 1: Binary Search ──────────────────────────────────────────────────
# Given a SORTED list and a target, return the index of target or -1.
# O(log n) — halves the search space each step.
#
# Use case: finding a threshold in a sorted list of eval scores,
# locating a version in a sorted release list.

def binary_search(arr: list[int], target: int) -> int:
    pass


# ── Problem 2: Binary Search — First Bad Version ──────────────────────────────
# Classic variant. Given n versions [1..n], and a function is_bad(version)
# that returns True for all versions >= the first bad one,
# find the FIRST bad version using minimum calls to is_bad().
#
# Example: n=5, bad starts at version 3
# is_bad(3)=True, is_bad(4)=True, is_bad(5)=True
# is_bad(1)=False, is_bad(2)=False
# → return 3
#
# Real-world: bisect a CI pipeline to find which commit broke the build.

def first_bad_version(n: int, is_bad: callable) -> int:
    pass


# ── Problem 3: Merge Sort ──────────────────────────────────────────────────────
# Implement merge sort. O(n log n), stable, divide-and-conquer.
# You won't be asked to implement this often, but understanding it
# shows algorithmic depth.
#
# Steps:
# 1. Split list in half recursively until size 1
# 2. Merge two sorted halves by comparing elements one by one

def merge_sort(arr: list[int]) -> list[int]:
    pass


def merge(left: list[int], right: list[int]) -> list[int]:
    """Merge two sorted lists into one sorted list."""
    pass


# ── Problem 4: Search in Rotated Sorted Array ─────────────────────────────────
# A sorted array was rotated at some pivot. Find target or return -1.
# Example: [4,5,6,7,0,1,2], target=0 → 4
# Constraint: O(log n) — must use binary search variant.
#
# Key insight: one half of the array is always sorted.
# Use that to decide which half to search.

def search_rotated(arr: list[int], target: int) -> int:
    pass


# ── Self-check ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Binary Search ===")
    print(binary_search([1, 3, 5, 7, 9, 11], 7))    # 3
    print(binary_search([1, 3, 5, 7, 9, 11], 6))    # -1
    print(binary_search([], 1))                       # -1

    print("\n=== First Bad Version ===")
    # Versions 1-5, bad starts at 3
    bad_from = 3
    print(first_bad_version(5, lambda v: v >= bad_from))  # 3
    print(first_bad_version(1, lambda v: v >= 1))          # 1

    print("\n=== Merge Sort ===")
    print(merge_sort([5, 2, 8, 1, 9, 3]))    # [1, 2, 3, 5, 8, 9]
    print(merge_sort([]))                     # []
    print(merge_sort([1]))                    # [1]

    print("\n=== Search Rotated ===")
    print(search_rotated([4,5,6,7,0,1,2], 0))   # 4
    print(search_rotated([4,5,6,7,0,1,2], 3))   # -1
    print(search_rotated([1], 0))                # -1
