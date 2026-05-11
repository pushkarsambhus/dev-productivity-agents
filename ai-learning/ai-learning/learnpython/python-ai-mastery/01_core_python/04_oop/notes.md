# Notes: OOP

## Class vs Dataclass — When to Use Which

| | `class` | `@dataclass` |
|---|---|---|
| Boilerplate | Manual `__init__`, `__repr__` | Auto-generated |
| Custom logic | Full control | Add methods freely |
| Immutable | Manual | `frozen=True` |
| Use when | Behavior-heavy objects | Data containers |

```python
from dataclasses import dataclass, field

@dataclass
class EvalResult:
    name: str
    score: float
    tags: list[str] = field(default_factory=list)   # mutable default
```

---

## ABC Pattern

```python
from abc import ABC, abstractmethod

class BaseEvaluator(ABC):
    @abstractmethod
    def evaluate(self, response: str) -> float:
        pass   # subclasses MUST implement this

# Trying to instantiate BaseEvaluator() raises TypeError
```

Use ABCs when you want to enforce a contract across multiple implementations (different LLM evaluators, different vector stores, etc.).

---

## Property vs Attribute

```python
class TokenBudget:
    def __init__(self, budget):
        self.budget = budget
        self.used = 0

    @property
    def remaining(self):
        return self.budget - self.used   # computed, never stale

# budget.remaining — looks like attribute, behaves like method call
# budget.remaining = 5 — raises AttributeError (read-only)
```

Use `@property` for values derived from other state. Avoids sync bugs from storing redundant data.

---

## Dunder Methods Cheat Sheet

| Method | Triggered by |
|--------|-------------|
| `__init__` | `MyClass()` |
| `__repr__` | `repr(obj)`, `print(obj)` in REPL |
| `__str__` | `str(obj)`, `print(obj)` |
| `__len__` | `len(obj)` |
| `__bool__` | `if obj:` |
| `__eq__` | `obj == other` |
| `__lt__` | `obj < other`, `sorted()` |
| `__contains__` | `x in obj` |
| `__iter__` | `for x in obj:` |
| `__enter__`/`__exit__` | `with obj:` |

---

## `super()` Pattern

```python
class Child(Parent):
    def __init__(self, x, y):
        super().__init__(x)   # call Parent.__init__ first
        self.y = y            # then extend
```

Always call `super().__init__()` in subclass `__init__` unless you have a specific reason not to.

---

## Interview Tip
At principal level you won't be asked "what is inheritance" — you'll be asked to design a class hierarchy for a real problem. Know when to use: composition over inheritance, ABC for contracts, dataclass for DTOs, `@property` for computed state.
