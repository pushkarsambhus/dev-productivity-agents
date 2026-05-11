# Notes: Hashmaps & Sets

## The Hashmap Pattern

> "Store what you've seen. Look up what you need."

```python
# Two Sum template:
seen = {}
for i, num in enumerate(nums):
    complement = target - num
    if complement in seen:
        return [seen[complement], i]
    seen[num] = i
```

This pattern solves ~40% of medium array/string problems.

---

## Set Operations

```python
a = {1, 2, 3}
b = {2, 3, 4}

a | b    # union:        {1, 2, 3, 4}
a & b    # intersection: {2, 3}
a - b    # difference:   {1}  (in a but not b)
a ^ b    # symmetric:    {1, 4}  (in either but not both)

# Membership check: O(1)
x in a   # True/False
```

---

## Counter Patterns

```python
from collections import Counter

c = Counter([1, 1, 2, 3, 3, 3])
c.most_common(2)    # [(3, 3), (1, 2)]
c[99]               # 0 — no KeyError for missing keys
c + Counter([1])    # add counts
c - Counter([1])    # subtract counts (drops zeros/negatives)

# Anagram check:
Counter("eat") == Counter("tea")   # True
```

---

## defaultdict vs dict.get()

```python
# dict.get(): one-off safe lookup with default
val = d.get("key", 0)

# defaultdict: when you're building a structure iteratively
from collections import defaultdict
d = defaultdict(list)
for item in items:
    d[item.category].append(item)   # no KeyError, auto-initializes

# setdefault(): middle ground
d.setdefault("key", []).append(val)
```

---

## Hashability Rules
Only hashable objects can be dict keys or set members:
- ✅ Hashable: `str`, `int`, `float`, `bool`, `tuple` (of hashables), `frozenset`
- ❌ Not hashable: `list`, `dict`, `set`

```python
# Can't use list as key:
d[["a", "b"]] = 1   # TypeError

# Fix: convert to tuple
d[tuple(["a", "b"])] = 1   # works
```

---

## Interview Tip
Before writing any nested loop, ask: "Can I use a hashmap to bring this from O(n²) to O(n)?" The answer is yes surprisingly often. The key is identifying what to store and what to look up.
