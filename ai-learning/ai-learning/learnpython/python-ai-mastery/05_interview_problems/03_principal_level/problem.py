"""
PHASE 5 | INTERVIEW PROBLEMS | 03 PRINCIPAL LEVEL
==================================================
Problem: LLM Pipeline Task Scheduler
Difficulty: Principal / Staff Engineer

Context: You're designing a lightweight DAG-based task runner for an LLM pipeline.
Each task has dependencies. Tasks can only run when all their dependencies are done.
This is exactly the kind of problem Workday's Flowise team would discuss.

This is a topological sort problem — appears in:
- CI/CD pipeline scheduling
- LLM agent orchestration (LangGraph, Flowise DAGs)
- Build systems (Make, Bazel)

Your job: implement the scheduler.
"""
from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Task:
    name: str
    fn: callable                        # the work this task does
    depends_on: list[str] = field(default_factory=list)
    result: Any = None


class PipelineScheduler:
    """
    Runs a DAG of tasks in dependency order.
    Tasks with no dependencies run first.
    Tasks whose dependencies are all complete run next, etc.
    """

    def __init__(self):
        self.tasks: dict[str, Task] = {}

    def add_task(self, task: Task):
        """Register a task."""
        # TODO: store in self.tasks by name
        pass

    def _build_graph(self) -> tuple[dict, dict]:
        """
        Build adjacency list and in-degree count for topological sort.
        Returns: (adjacency: {task → [dependents]}, in_degree: {task → count})
        """
        # TODO:
        # in_degree[task] = number of tasks it depends on
        # adjacency[dep] = list of tasks that depend on dep
        pass

    def run(self) -> dict[str, Any]:
        """
        Execute tasks in topological order (Kahn's algorithm).
        Returns dict of task_name → result.
        Raises ValueError if a cycle is detected.
        """
        # TODO:
        # 1. Build graph with _build_graph()
        # 2. Start queue with all tasks that have in_degree == 0
        # 3. While queue not empty:
        #    a. Pop task from queue
        #    b. Run task.fn() — pass results of dependencies as kwargs
        #    c. Store result
        #    d. For each dependent: decrement in_degree, if 0 → add to queue
        # 4. If processed count < total tasks → cycle detected, raise ValueError
        pass


# ── Self-check ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Simulate an LLM pipeline:
    # fetch_docs → embed_docs → retrieve_chunks ──┐
    #                                              ├─→ generate_answer → format_output
    # load_prompt ─────────────────────────────────┘

    scheduler = PipelineScheduler()
    results_store = {}

    scheduler.add_task(Task("fetch_docs",     lambda: ["doc1", "doc2", "doc3"]))
    scheduler.add_task(Task("load_prompt",    lambda: "Answer this: {question}"))
    scheduler.add_task(Task("embed_docs",     lambda: [[0.1, 0.2], [0.3, 0.4]], depends_on=["fetch_docs"]))
    scheduler.add_task(Task("retrieve_chunks",lambda: ["chunk_a", "chunk_b"],    depends_on=["embed_docs"]))
    scheduler.add_task(Task("generate_answer",lambda: "42 is the answer.",       depends_on=["retrieve_chunks", "load_prompt"]))
    scheduler.add_task(Task("format_output",  lambda: "**Answer:** 42 is the answer.", depends_on=["generate_answer"]))

    results = scheduler.run()
    print("Pipeline results:")
    for name, result in results.items():
        print(f"  {name}: {result}")

    # Cycle detection test
    print("\n=== Cycle detection ===")
    bad = PipelineScheduler()
    bad.add_task(Task("a", lambda: 1, depends_on=["b"]))
    bad.add_task(Task("b", lambda: 2, depends_on=["a"]))
    try:
        bad.run()
    except ValueError as e:
        print(f"Caught expected error: {e}")
