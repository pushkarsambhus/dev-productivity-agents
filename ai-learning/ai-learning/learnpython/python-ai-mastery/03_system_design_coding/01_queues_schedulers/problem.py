"""
PHASE 3 | SYSTEM DESIGN CODING | 01 QUEUES & SCHEDULERS
========================================================
Topic: Priority queues, task scheduling, worker pools.
This is a direct analogue to CI/CD pipeline schedulers and LLM job queues.

You discussed a version of this in your Workday Flowise interview:
1M concurrent agent executions → Kafka + Kubernetes + Redis.
This module builds the Python-level foundation beneath that.
"""
import heapq
import time
from dataclasses import dataclass, field
from enum import IntEnum
from collections import deque
from threading import Thread, Lock
import queue


# ── Priority levels ────────────────────────────────────────────────────────────
class Priority(IntEnum):
    HIGH   = 1
    MEDIUM = 2
    LOW    = 3


# ── Problem 1: Priority Queue ─────────────────────────────────────────────────
# Implement a priority queue for LLM jobs.
# Higher priority jobs run first. For same priority: FIFO.
# Use Python's heapq module (min-heap).

@dataclass(order=True)
class Job:
    priority: int           # lower number = higher priority (min-heap)
    sequence: int           # tiebreaker: lower = enqueued earlier
    job_id: str = field(compare=False)
    payload: dict = field(compare=False, default_factory=dict)


class JobQueue:
    def __init__(self):
        # TODO: initialize a heap list and a sequence counter
        pass

    def push(self, job_id: str, priority: Priority, payload: dict = None) -> Job:
        """
        Add a job. Returns the Job that was added.
        TODO: create a Job with current sequence number, push to heap via heapq.heappush
        """
        pass

    def pop(self) -> Job | None:
        """Remove and return highest-priority job. Return None if empty."""
        # TODO: use heapq.heappop, return None if heap is empty
        pass

    def peek(self) -> Job | None:
        """Return highest-priority job without removing it."""
        pass

    def __len__(self) -> int:
        pass


# ── Problem 2: Simple Worker Pool ─────────────────────────────────────────────
# A worker pool processes jobs from a queue concurrently.
# Uses Python's threading + queue.Queue (thread-safe).
#
# TODO: Complete the WorkerPool class.

class WorkerPool:
    """
    Fixed-size thread pool that processes jobs from a queue.

    Args:
        num_workers: number of worker threads
        handler: function called for each job dict
    """

    def __init__(self, num_workers: int, handler: callable):
        self.num_workers = num_workers
        self.handler = handler
        self._queue = queue.Queue()
        self._workers: list[Thread] = []
        self._running = False

    def start(self):
        """Start worker threads."""
        # TODO:
        # Set _running = True
        # Create num_workers threads, each running _worker_loop
        # Set each thread as daemon=True (dies when main thread exits)
        # Start each thread, store in _workers
        pass

    def _worker_loop(self):
        """Each worker runs this loop: get job, process, repeat."""
        # TODO:
        # While _running:
        #   Try to get a job from _queue with timeout=0.1
        #   If got one: call self.handler(job)
        #   On queue.Empty: continue (timeout hit, check _running again)
        pass

    def submit(self, job: dict):
        """Add a job to the queue."""
        # TODO
        pass

    def stop(self, wait: bool = True):
        """Signal workers to stop. If wait=True, join all threads."""
        # TODO
        pass


# ── Problem 3: Scheduled Task Runner ─────────────────────────────────────────
# Run tasks at a scheduled future time (Unix timestamp).
# Uses a min-heap ordered by run_at time.

@dataclass(order=True)
class ScheduledTask:
    run_at: float           # Unix timestamp
    task_id: str = field(compare=False)
    fn: callable = field(compare=False)


class Scheduler:
    """
    Simple task scheduler. Tasks are added with a delay (seconds from now).
    Call tick() to run any tasks whose time has come.
    """

    def __init__(self):
        # TODO: heap of ScheduledTasks
        pass

    def schedule(self, task_id: str, fn: callable, delay_seconds: float):
        """Schedule fn to run after delay_seconds."""
        # TODO: compute run_at = now + delay, push to heap
        pass

    def tick(self) -> list[str]:
        """
        Run all tasks whose run_at <= now.
        Returns list of task_ids that were executed.
        """
        # TODO: while heap and heap[0].run_at <= now: pop and call fn()
        pass

    def pending_count(self) -> int:
        pass


# ── Self-check ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Job Queue ===")
    jq = JobQueue()
    jq.push("job-1", Priority.LOW,    {"prompt": "low priority task"})
    jq.push("job-2", Priority.HIGH,   {"prompt": "urgent eval"})
    jq.push("job-3", Priority.MEDIUM, {"prompt": "normal task"})
    jq.push("job-4", Priority.HIGH,   {"prompt": "another urgent"})

    print(f"Queue size: {len(jq)}")
    while len(jq):
        job = jq.pop()
        print(f"  Processing: [{Priority(job.priority).name}] {job.job_id}")
    # Expected order: job-2, job-4, job-3, job-1

    print("\n=== Worker Pool ===")
    results = []
    lock = Lock()

    def handle_job(job: dict):
        with lock:
            results.append(job["id"])

    pool = WorkerPool(num_workers=2, handler=handle_job)
    pool.start()
    for i in range(6):
        pool.submit({"id": f"task-{i}"})
    time.sleep(0.2)  # let workers process
    pool.stop()
    print(f"Processed {len(results)} jobs: {sorted(results)}")

    print("\n=== Scheduler ===")
    log = []
    sched = Scheduler()
    sched.schedule("task-a", lambda: log.append("a"), delay_seconds=0.0)
    sched.schedule("task-b", lambda: log.append("b"), delay_seconds=0.05)
    sched.schedule("task-c", lambda: log.append("c"), delay_seconds=10.0)

    ran = sched.tick()
    print(f"Ran immediately: {ran}")          # ['task-a']
    time.sleep(0.1)
    ran = sched.tick()
    print(f"Ran after 0.1s: {ran}")           # ['task-b']
    print(f"Still pending: {sched.pending_count()}")  # 1 (task-c)
