# Notes: Sorting & Searching

## Binary Search Template (memorize this exactly)

```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:                        # ← <= not <
        mid = left + (right - left) // 2        # ← avoids overflow
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

The `mid = left + (right - left) // 2` form prevents integer overflow. In Python integers don't overflow, but write it this way anyway — interviewers notice.

---

## Binary Search Variants

### Find leftmost position satisfying condition (e.g. first bad version)
```python
left, right = 0, n
while left < right:              # ← < not <=
    mid = left + (right - left) // 2
    if is_bad(mid):
        right = mid              # ← not mid-1
    else:
        left = mid + 1
return left                      # left == right == answer
```

### Find rightmost valid position
```python
while left < right:
    mid = left + (right - left + 1) // 2   # ← ceiling division
    if is_valid(mid):
        left = mid               # ← not mid+1
    else:
        right = mid - 1
return left
```

---

## Python's Built-in bisect

```python
import bisect
arr = [1, 3, 5, 7, 9]

bisect.bisect_left(arr, 5)    # 2 — index of first element >= 5
bisect.bisect_right(arr, 5)   # 3 — index of first element > 5
bisect.insort(arr, 6)         # inserts 6 in sorted position: O(n)
```

Use `bisect` in production instead of rolling your own. Know what it does for interviews.

---

## Sorting Complexity

| Algorithm | Time | Space | Stable | Notes |
|-----------|------|-------|--------|-------|
| Timsort (Python built-in) | O(n log n) | O(n) | Yes | Hybrid merge+insertion |
| Merge sort | O(n log n) | O(n) | Yes | Divide and conquer |
| Quick sort | O(n log n) avg | O(log n) | No | In-place, cache-friendly |
| Heap sort | O(n log n) | O(1) | No | Used in heapq |
| Counting sort | O(n+k) | O(k) | Yes | Only for integers in range k |

---

## Python Sort Patterns

```python
# Sort list in place
nums.sort()
nums.sort(reverse=True)
nums.sort(key=lambda x: x["score"])

# Return new sorted list
sorted(nums)
sorted(items, key=lambda x: (-x["priority"], x["name"]))

# Sort stability: equal elements keep original order
# Python's sort is always stable — safe to sort by multiple criteria sequentially
```

---

## Interview Tip
Binary search applies beyond sorted arrays: any problem where you can test "is X too high / too low?" and the answer is monotonic can use binary search. Examples: "minimum capacity to ship packages in D days", "find peak element", "search in rotated array." The pattern is: define your search space, define your condition, halve appropriately.
