"""
SOLUTION: Phase 2 | Algorithms & DS | 05 Sorting & Searching
"""

# ── Problem 1: Binary Search ──────────────────────────────────────────────────
def binary_search(arr: list[int], target: int) -> int:
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = left + (right - left) // 2   # avoids integer overflow vs (l+r)//2
        if arr[mid] == target:
            return mid
        if arr[mid] < target:
            left = mid + 1    # target is in right half
        else:
            right = mid - 1   # target is in left half
    return -1
    # Template: left <= right, mid = left + (right-left)//2
    # Memorize this — the off-by-one errors in binary search are notorious.


# ── Problem 2: First Bad Version ──────────────────────────────────────────────
def first_bad_version(n: int, is_bad: callable) -> int:
    left, right = 1, n
    while left < right:           # note: < not <=
        mid = left + (right - left) // 2
        if is_bad(mid):
            right = mid           # bad version could be mid or earlier
        else:
            left = mid + 1        # mid is good, bad must be after
    return left                   # left == right == first bad version
    # Variant: finding the LEFTMOST position that satisfies a condition.
    # Pattern: when is_bad(mid) → right=mid (not mid-1), loop ends at left==right.


# ── Problem 3: Merge Sort ─────────────────────────────────────────────────────
def merge_sort(arr: list[int]) -> list[int]:
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left  = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)


def merge(left: list[int], right: list[int]) -> list[int]:
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    # Append remaining elements (one of these will be empty)
    result.extend(left[i:])
    result.extend(right[j:])
    return result
    # extend() vs append(): extend adds all items, append adds one item (the list itself)


# ── Problem 4: Search in Rotated Sorted Array ─────────────────────────────────
def search_rotated(arr: list[int], target: int) -> int:
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == target:
            return mid
        # Left half is sorted
        if arr[left] <= arr[mid]:
            if arr[left] <= target < arr[mid]:
                right = mid - 1   # target is in sorted left half
            else:
                left = mid + 1    # target is in right half
        # Right half is sorted
        else:
            if arr[mid] < target <= arr[right]:
                left = mid + 1    # target is in sorted right half
            else:
                right = mid - 1   # target is in left half
    return -1
    # Key insight: in any rotation, at least ONE half is always sorted.
    # Check if target falls in the sorted half → search there. Otherwise flip.


# ── Interview talking points ───────────────────────────────────────────────────
"""
Python's built-in sort:
  sorted() and list.sort() use Timsort — O(n log n) worst case, O(n) best case.
  Timsort is a hybrid merge sort + insertion sort, optimized for real data.
  You'll almost never implement sort from scratch in production — but knowing
  merge sort proves you understand divide-and-conquer.

Binary search library:
  import bisect
  bisect.bisect_left(arr, target)  → leftmost insertion point
  bisect.bisect_right(arr, target) → rightmost insertion point
  Use this in production instead of rolling your own.

When do you actually use binary search in AI systems?
  - Threshold tuning: find minimum confidence score that gives recall >= 0.9
  - Version bisection: first_bad_version IS the git bisect algorithm
  - Top-k retrieval: binary search on score threshold in a sorted results list
"""

if __name__ == "__main__":
    print("=== Binary Search ===")
    print(binary_search([1, 3, 5, 7, 9, 11], 7))
    print(binary_search([1, 3, 5, 7, 9, 11], 6))
    print(binary_search([], 1))

    print("\n=== First Bad Version ===")
    bad_from = 3
    print(first_bad_version(5, lambda v: v >= bad_from))
    print(first_bad_version(1, lambda v: v >= 1))

    print("\n=== Merge Sort ===")
    print(merge_sort([5, 2, 8, 1, 9, 3]))
    print(merge_sort([]))
    print(merge_sort([1]))

    print("\n=== Search Rotated ===")
    print(search_rotated([4,5,6,7,0,1,2], 0))
    print(search_rotated([4,5,6,7,0,1,2], 3))
    print(search_rotated([1], 0))
