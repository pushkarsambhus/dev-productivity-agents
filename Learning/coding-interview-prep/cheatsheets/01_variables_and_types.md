# Variables & Types

**Pattern: TYPE AWARENESS** — Before doing anything with a variable, know its type. Wrong type = runtime crash.

---

## The 4 basic types

| Type | Example | Java equivalent |
|------|---------|-----------------|
| `int` | `age = 25` | `int age = 25;` |
| `float` | `price = 9.99` | `double price = 9.99;` |
| `str` | `name = "Alice"` | `String name = "Alice";` |
| `bool` | `active = True` | `boolean active = true;` |

**Key difference from Java:** Python is dynamically typed — no type declarations. Type is inferred at runtime. You are the compiler.

---

## Type casting

```python
str(25)        # → "25"
int(9.99)      # → 9   (truncates, never rounds)
float("3.14")  # → 3.14
```

## Check the type

```python
type(25)       # → <class 'int'>   (returns the class, not the value)
```

---

## Gotchas

- `type()` returns `<class 'int'>` — not the value itself
- `int(3.7)` → `3`, not `4` — always truncates toward zero
- `print("x:", val)` adds a space — use f-strings: `f"x: {val}"`

---

## Interview trigger

> "Given a string input, do math with it" → cast first with `int()` or `float()`, then operate
