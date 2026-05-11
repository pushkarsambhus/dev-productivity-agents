"""
SOLUTION: Phase 5 | Interview Problems | Principal Level
Problem: LLM Pipeline Task Scheduler (Topological Sort / Kahn's Algorithm)
"""
from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Task:
    name: str
    fn: callable
    depends_on: list[str] = field(default_factory=list)
    result: Any = None


class PipelineScheduler:

    def __init__(self):
        self.tasks: dict[str, Task] = {}

    def add_task(self, task: Task):
        self.tasks[task.name] = task

    def _build_graph(self) -> tuple[dict, dict]:
        in_degree = {name: 0 for name in self.tasks}
        adjacency = defaultdict(list)

        for name, task in self.tasks.items():
            for dep in task.depends_on:
                adjacency[dep].append(name)   # dep → [tasks that need dep]
                in_degree[name] += 1          # this task needs one more thing done first

        return adjacency, in_degree

    def run(self) -> dict[str, Any]:
        adjacency, in_degree = self._build_graph()

        # Start with tasks that have no dependencies
        queue = deque(name for name, deg in in_degree.items() if deg == 0)
        results = {}
        processed = 0

        while queue:
            name = queue.popleft()
            task = self.tasks[name]

            # Run the task
            task.result = task.fn()
            results[name] = task.result
            processed += 1

            # Unblock dependents
            for dependent in adjacency[name]:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)

        if processed < len(self.tasks):
            raise ValueError(
                f"Cycle detected in pipeline — only {processed}/{len(self.tasks)} tasks completed"
            )

        return results


# ── Interview talking points ───────────────────────────────────────────────────
"""
Complexity:
  Time:  O(V + E)  — V=tasks, E=dependency edges
  Space: O(V + E)  — adjacency list + queue

Q: How would you parallelize this?
A: Tasks with in_degree == 0 at the same time can run in parallel.
   Use asyncio.gather() or a ThreadPoolExecutor.
   Each completed task decrements dependents' in_degree — use a lock or
   asyncio-safe counter to avoid race conditions.

Q: How does LangGraph / Flowise handle this?
A: LangGraph uses a similar DAG execution model with StateGraph.
   Flowise wraps it with a visual UI. Under the hood it's topological sort
   with streaming support for partial results.

Q: What if a task fails?
A: Add retry logic (Phase 1, Exercise 5 pattern!), mark task as FAILED,
   and skip downstream dependents (or fail them too, depending on strategy).
   Production systems add: timeout, dead-letter queue, alerting.

Q: How does this relate to your build failure detection work?
A: Your LangChain pipeline that reduced triage from 20min → instant is
   a linear pipeline (chain). This generalizes it to arbitrary DAGs —
   exactly the jump from "automation engineer" to "AI platform engineer".
"""

if __name__ == "__main__":
    scheduler = PipelineScheduler()

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

    print("\n=== Cycle detection ===")
    bad = PipelineScheduler()
    bad.add_task(Task("a", lambda: 1, depends_on=["b"]))
    bad.add_task(Task("b", lambda: 2, depends_on=["a"]))
    try:
        bad.run()
    except ValueError as e:
        print(f"Caught expected error: {e}")
