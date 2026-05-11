"""
PHASE 1 | CORE PYTHON | 04 OOP
===============================
Topic: Classes, inheritance, dunder methods, dataclasses, properties.
AI frameworks are heavily OOP — LangChain, Pydantic models, eval harnesses.
"""
from dataclasses import dataclass, field
from abc import ABC, abstractmethod


# ── Exercise 1: Basic class with dunder methods ────────────────────────────────
# Model a token budget tracker for an LLM session.
# TODO: Implement the class below.

class TokenBudget:
    """Tracks token usage against a budget for an LLM session."""

    def __init__(self, budget: int):
        # TODO: store budget, initialize used=0
        pass

    def consume(self, tokens: int):
        """Add tokens to used count."""
        # TODO: raise ValueError if consuming would exceed budget
        pass

    @property
    def remaining(self) -> int:
        """Tokens still available."""
        pass  # TODO

    def __repr__(self) -> str:
        # TODO: return e.g. "TokenBudget(used=150/1000, remaining=850)"
        pass

    def __bool__(self) -> bool:
        # TODO: return True if there are tokens remaining
        pass


# ── Exercise 2: Inheritance + ABC ─────────────────────────────────────────────
# Build a simple evaluator class hierarchy.
# All evaluators must implement evaluate(response: str) -> float

class BaseEvaluator(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def evaluate(self, response: str) -> float:
        """Return a score between 0.0 and 1.0"""
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}')"


# TODO: Implement LengthEvaluator — scores 1.0 if response is between
# min_len and max_len chars, 0.0 otherwise.
class LengthEvaluator(BaseEvaluator):
    def __init__(self, min_len: int, max_len: int):
        super().__init__("length_check")
        # TODO
        pass

    def evaluate(self, response: str) -> float:
        pass


# TODO: Implement KeywordEvaluator — scores the fraction of required_keywords
# found in the response (case-insensitive).
class KeywordEvaluator(BaseEvaluator):
    def __init__(self, required_keywords: list[str]):
        super().__init__("keyword_coverage")
        # TODO
        pass

    def evaluate(self, response: str) -> float:
        pass


# ── Exercise 3: Dataclass ──────────────────────────────────────────────────────
# TODO: Define a dataclass `EvalRun` that represents one complete eval run.
# Fields: run_id (str), model (str), scores (list of floats, default empty),
#         metadata (dict, default empty)
# Add a method `average_score()` that returns the mean of scores (0.0 if empty).

@dataclass
class EvalRun:
    pass  # TODO


# ── Self-check ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== TokenBudget ===")
    budget = TokenBudget(1000)
    budget.consume(150)
    print(budget)                    # TokenBudget(used=150/1000, remaining=850)
    print(bool(budget))              # True
    budget.consume(850)
    print(bool(budget))              # False
    try:
        budget.consume(1)            # should raise ValueError
    except ValueError as e:
        print(f"Caught: {e}")

    print("\n=== Evaluators ===")
    le = LengthEvaluator(min_len=10, max_len=200)
    print(le.evaluate("Short"))                   # 0.0
    print(le.evaluate("This is a valid response that is long enough."))  # 1.0

    ke = KeywordEvaluator(["refund", "policy", "30 days"])
    print(ke.evaluate("Our refund policy covers 30 days."))  # 1.0
    print(ke.evaluate("We offer returns."))                   # 0.0

    print("\n=== EvalRun ===")
    run = EvalRun(run_id="run_001", model="claude-3-sonnet", scores=[0.9, 0.85, 1.0])
    print(run)
    print(f"Average: {run.average_score():.2f}")  # 0.92
