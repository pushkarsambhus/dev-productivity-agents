"""
SOLUTION: Phase 1 | Core Python | 04 OOP
"""
from dataclasses import dataclass, field
from abc import ABC, abstractmethod


# ── Exercise 1 ─────────────────────────────────────────────────────────────────
class TokenBudget:
    def __init__(self, budget: int):
        self.budget = budget
        self.used = 0

    def consume(self, tokens: int):
        if self.used + tokens > self.budget:
            raise ValueError(
                f"Cannot consume {tokens} tokens — only {self.remaining} remaining"
            )
        self.used += tokens

    @property
    def remaining(self) -> int:
        return self.budget - self.used
    # @property lets you call budget.remaining like an attribute, not budget.remaining()
    # Computed properties > storing redundant state (avoids sync bugs)

    def __repr__(self) -> str:
        return f"TokenBudget(used={self.used}/{self.budget}, remaining={self.remaining})"

    def __bool__(self) -> bool:
        return self.remaining > 0
    # __bool__ lets you write: if budget: ... instead of if budget.remaining > 0: ...


# ── Exercise 2 ─────────────────────────────────────────────────────────────────
class BaseEvaluator(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def evaluate(self, response: str) -> float:
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}')"


class LengthEvaluator(BaseEvaluator):
    def __init__(self, min_len: int, max_len: int):
        super().__init__("length_check")
        self.min_len = min_len
        self.max_len = max_len

    def evaluate(self, response: str) -> float:
        return 1.0 if self.min_len <= len(response) <= self.max_len else 0.0
        # Chained comparison: min <= x <= max is idiomatic Python


class KeywordEvaluator(BaseEvaluator):
    def __init__(self, required_keywords: list[str]):
        super().__init__("keyword_coverage")
        self.required_keywords = [kw.lower() for kw in required_keywords]

    def evaluate(self, response: str) -> float:
        response_lower = response.lower()
        found = sum(1 for kw in self.required_keywords if kw in response_lower)
        return round(found / len(self.required_keywords), 2)


# ── Exercise 3 ─────────────────────────────────────────────────────────────────
@dataclass
class EvalRun:
    run_id: str
    model: str
    scores: list[float] = field(default_factory=list)    # mutable default — use field()
    metadata: dict = field(default_factory=dict)         # same here

    def average_score(self) -> float:
        return round(sum(self.scores) / len(self.scores), 2) if self.scores else 0.0
    # Conditional expression: value_if_true if condition else value_if_false
    # Avoids ZeroDivisionError when scores list is empty


if __name__ == "__main__":
    print("=== TokenBudget ===")
    budget = TokenBudget(1000)
    budget.consume(150)
    print(budget)
    print(bool(budget))
    budget.consume(850)
    print(bool(budget))
    try:
        budget.consume(1)
    except ValueError as e:
        print(f"Caught: {e}")

    print("\n=== Evaluators ===")
    le = LengthEvaluator(min_len=10, max_len=200)
    print(le.evaluate("Short"))
    print(le.evaluate("This is a valid response that is long enough."))

    ke = KeywordEvaluator(["refund", "policy", "30 days"])
    print(ke.evaluate("Our refund policy covers 30 days."))
    print(ke.evaluate("We offer returns."))

    print("\n=== EvalRun ===")
    run = EvalRun(run_id="run_001", model="claude-3-sonnet", scores=[0.9, 0.85, 1.0])
    print(run)
    print(f"Average: {run.average_score():.2f}")
