# Notes: Data Structures

## The Big Four

| Structure | Use When | Key Method | Gotcha |
|-----------|----------|------------|--------|
| `list` | ordered, indexed, mutable | `append`, `pop`, `sort` | `pop(0)` is O(n) — use deque |
| `dict` | key→value lookup | `.get(k, default)`, `.items()` | mutable default = shared state bug |
| `set` | deduplication, membership | `in`, `|`, `&`, `-` | unordered — no indexing |
| `tuple` | immutable record, dict key | unpacking | can't be changed — use as hashmap key |

---

## Patterns That Appear Constantly

### Accumulate into a dict
```python
# BAD
if key not in d:
    d[key] = []
d[key].append(val)

# GOOD
from collections import defaultdict
d = defaultdict(list)
d[key].append(val)   # auto-initializes
```

### Dict comprehension
```python
{k: v for k, v in items.items() if condition}
```

### Flatten + deduplicate
```python
unique = sorted(set(item for sublist in nested for item in sublist))
```

### Tuple unpacking in loops
```python
for name, passed, _ in eval_results:   # _ = don't care
    ...
```

---

## collections module — use these, don't reinvent them

```python
from collections import defaultdict, Counter, deque, OrderedDict, namedtuple

Counter("aabbcc")          # {'a': 2, 'b': 2, 'c': 2}
Counter.most_common(3)     # top 3
defaultdict(int)           # auto-init to 0
defaultdict(list)          # auto-init to []
deque(maxlen=100)          # fixed-size circular buffer
OrderedDict()              # ordered + move_to_end()
```

---

## Interview Tip
When asked "how would you count X" or "group Y by Z" — the answer is almost always `Counter` or `defaultdict`. Reach for these before writing a for loop with if/else.
