# Notes: Core Python Basics

## Key Idioms to Internalize

### 1. Early Return (no-else-return)
```python
# BAD
def check(x):
    if x > 0:
        return "positive"
    else:
        return "non-positive"

# GOOD
def check(x):
    if x > 0:
        return "positive"
    return "non-positive"
```
Pylint flags the bad version as R1705. Once you return, the else is dead code.

### 2. Simplifiable Boolean
```python
# BAD
if condition:
    return True
else:
    return False

# GOOD
return bool(condition)   # or just: return condition  (if already bool)
```

### 3. List Comprehension
```python
# BAD (verbose)
result = []
for x in items:
    if x > 0:
        result.append(x * 2)

# GOOD
result = [x * 2 for x in items if x > 0]
```

### 4. f-strings
```python
name, val = "model", 0.92
print(f"{name} scored {val:.2%}")   # "model scored 92.00%"
print(f"{val:.4f}")                  # 4 decimal places
```

---

## Common Gotchas

- **Mutable default arguments**: `def fn(items=[])` — the list is shared across calls. Use `def fn(items=None): items = items or []`
- **Integer division**: `7 / 2 = 3.5` (float), `7 // 2 = 3` (int)
- **String immutability**: strings can't be changed in place — always reassign

---

## Interview Tip
At principal level, interviewers don't care if you remember `sorted()` params — they watch *how* you think. Talk through your logic before you write. Early returns and list comprehensions signal Python fluency.
