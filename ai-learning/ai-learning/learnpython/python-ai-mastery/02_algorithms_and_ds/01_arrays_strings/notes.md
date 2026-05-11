# Notes: Arrays & Strings

## The Two Core Templates

### Sliding Window (fixed size)
```python
# Max/min/avg of any k consecutive elements
window_sum = sum(arr[:k])
best = window_sum
for i in range(k, len(arr)):
    window_sum += arr[i] - arr[i - k]   # add new, drop old
    best = max(best, window_sum)
```

### Sliding Window (variable size)
```python
# Longest/shortest subarray satisfying a condition
left = 0
for right in range(len(arr)):
    # expand: include arr[right]
    while <constraint violated>:
        # shrink: exclude arr[left]
        left += 1
    best = max(best, right - left + 1)
```

### Two Pointers (sorted array)
```python
left, right = 0, len(arr) - 1
while left < right:
    if condition(arr[left], arr[right]):
        return result
    elif too_small:
        left += 1
    else:
        right -= 1
```

---

## When to Use Which

| Pattern | Signal words |
|---------|-------------|
| Sliding window (fixed) | "consecutive k elements", "subarray of size k" |
| Sliding window (variable) | "longest/shortest subarray with...", "no duplicate" |
| Two pointers | "sorted array", "pair that sums to", "palindrome check" |
| Hashmap | "count", "seen before", "two sum" |

---

## String Manipulation Cheat Sheet

```python
s.split()              # split on whitespace
s.split(",")           # split on comma
" ".join(words)        # join list into string
s.strip()              # remove leading/trailing whitespace
s.lower() / s.upper()
s.replace("old", "new")
s.startswith("pre") / s.endswith("suf")
s.isalnum()            # True if all alphanumeric (no spaces/punctuation)
s.find("sub")          # index of first match, -1 if not found
s[i:j]                 # slice: chars from i up to (not including) j
s[::-1]                # reverse
```

---

## Interview Tip
When you see "contiguous subarray" → think sliding window. When you see "sorted array" + "pair/sum" → think two pointers. Naming the pattern out loud before coding is what principal-level candidates do.
