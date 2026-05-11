# Notes: Pythonic Idioms

## The Pythonic Checklist

Before submitting any solution, ask yourself:
- [ ] Can I replace this `if/else: return True/False` with `return bool(expr)`?
- [ ] Can I replace this loop-and-append with a list comprehension?
- [ ] Am I using `.get(key, default)` instead of checking `key in dict`?
- [ ] Can I use `any()` / `all()` instead of a flag variable loop?
- [ ] Am I using `enumerate()` instead of a manual index?
- [ ] Am I using `zip()` to pair parallel lists?

---

## Generator vs List Comprehension

```python
# List comprehension — eager, builds entire list in memory
result = [process(x) for x in huge_list if condition(x)]

# Generator expression — lazy, one item at a time
result = (process(x) for x in huge_list if condition(x))

# Use next() to get just the first match — stops immediately
first = next((x for x in items if x["flagged"]), None)
```

**Rule of thumb:** If you only need the first item, or you're iterating once, use a generator. If you need to index into it or iterate multiple times, use a list.

---

## Unpacking Patterns

```python
first, *rest = [1, 2, 3, 4]          # first=1, rest=[2,3,4]
first, *middle, last = [1,2,3,4,5]   # first=1, middle=[2,3], last=5
a, b = b, a                           # swap without temp variable

# Unzip a list of tuples
pairs = [("a", 1), ("b", 2), ("c", 3)]
keys, values = zip(*pairs)            # keys=('a','b','c'), values=(1,2,3)
```

---

## Sorting — Lambda Key Patterns

```python
# Sort by single field
items.sort(key=lambda x: x["score"])

# Sort descending
items.sort(key=lambda x: x["score"], reverse=True)

# Sort by multiple fields: primary asc, secondary desc
items.sort(key=lambda x: (x["priority"], -x["score"]))

# Sort objects by attribute
items.sort(key=lambda x: x.name)
# or: from operator import attrgetter
items.sort(key=attrgetter("name"))
```

---

## String Formatting Quick Reference

```python
f"{value:.2f}"      # 2 decimal places: 3.14
f"{value:.2%}"      # percentage: 92.00%
f"{value:>10}"      # right-align in 10 chars
f"{value!r}"        # repr() — adds quotes around strings
f"{value:,}"        # thousands separator: 1,000,000
```

---

## Interview Tip
Pythonic code signals fluency. The difference between a mid-level and principal-level Python engineer is often just knowing: list comprehensions, generators, `zip`/`enumerate`, `any`/`all`, and the `collections` module. These are fast to write AND fast to read — interviewers notice.
