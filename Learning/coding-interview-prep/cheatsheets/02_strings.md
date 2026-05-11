# Strings

**Pattern: STRING MANIPULATION** — Strings are immutable sequences. Learn the built-ins; don't reinvent them.

---

## Common methods

```python
s = "Hello, World!"

s.upper()             # "HELLO, WORLD!"      → Java: s.toUpperCase()
s.lower()             # "hello, world!"      → Java: s.toLowerCase()
s.strip()             # removes whitespace   → Java: s.trim()
s.replace("a", "b")  # replaces all         → Java: s.replace()
s.split(",")          # splits into list     → Java: s.split()
s.startswith("He")    # True                 → Java: s.startsWith()
s.endswith("!")       # True                 → Java: s.endsWith()
s.find("World")       # index, -1 if missing → Java: s.indexOf()
s.title()             # Capitalizes Each Word (no Java equivalent)
len(s)                # length               → Java: s.length()
"World" in s          # True — substring check → Java: s.contains()
```

---

## Slicing — Python only

```python
s[0:5]    # "Hello"  — start inclusive, stop exclusive
s[-5:]    # last 5 chars — negative counts from end
s[::-1]   # reverse the string
s[::2]    # every other character
```

**Rule:** `[start : stop : step]` — start is **in**, stop is **out**

---

## f-strings

```python
name = "Alice"
score = 95
f"Hello, {name}! Score: {score}"
# Java: "Hello, " + name + "! Score: " + score
```

---

## Immutability

```python
s[0] = "h"        # TypeError — cannot modify in place
s = "h" + s[1:]   # must create a new string (same as Java)
```

---

## Gotchas

- `find()` returns `-1` if not found (safe). `index()` raises `ValueError` (crashes). Use `find()` when unsure.
- `s[-1]` is the last character, not index `0`
- Method chaining works: `s.strip().upper().replace("A", "B")`

---

## Interview classics

```python
s[::-1]                    # reverse a string
s.title()                  # capitalize each word
" ".join(["a","b","c"])    # join list into string → "a b c"
len(s)                     # always useful for boundary checks
```

## Interview trigger

> "Reverse", "palindrome", "count characters", "check substring" → reach for slicing + string methods
