"""
SOLUTION: Phase 3 | System Design Coding | 01 Queues & Schedulers
"""
import heapq
import time
import queue
from dataclasses import dataclass, field
from enum import IntEnum
from threading import Thread, Lock


class Priority(IntEnum):
    HIGH   = 1
    MEDIUM = 2
    LOW    = 3


@dataclass(order=True)
class Job:
    priority: int
    sequence: int
    job_id: str = field(compare=False)
    payload: dict = field(compare=False, default_factory=dict)


# ── Problem 1 ─────────────────────────────────────────────────────────────────
class JobQueue:
    def __init__(self):
        self._heap: list[Job] = []
        self._seq = 0

    def push(self, job_id: str, priority: Priority, payload: dict = None) -> Job:
        job = Job(priority=int(priority), sequence=self._seq,
                  job_id=job_id, payload=payload or {})
        heapq.heappush(self._heap, job)
        self._seq += 1
        return job
        # heapq is a MIN-heap: smallest value at top.
        # Priority.HIGH=1 < Priority.LOW=3, so HIGH jobs come out first. ✓
        # sequence as tiebreaker: lower sequence = enqueued earlier = FIFO within tier.

    def pop(self) -> Job | None:
        return heapq.heappop(self._heap) if self._heap else None

    def peek(self) -> Job | None:
        return self._heap[0] if self._heap else None

    def __len__(self) -> int:
        return len(self._heap)


# ── Problem 2 ─────────────────────────────────────────────────────────────────
class WorkerPool:
    def __init__(self, num_workers: int, handler: callable):
        self.num_workers = num_workers
        self.handler = handler
        self._queue = queue.Queue()
        self._workers: list[Thread] = []
        self._running = False

    def start(self):
        self._running = True
        for _ in range(self.num_workers):
            t = Thread(target=self._worker_loop, daemon=True)
            t.start()
            self._workers.append(t)

    def _worker_loop(self):
        while self._running:
            try:
                job = self._queue.get(timeout=0.1)  # blocks up to 0.1s
                self.handler(job)
                self._queue.task_done()
            except queue.Empty:
                continue   # timeout — check _running flag again

    def submit(self, job: dict):
        self._queue.put(job)

    def stop(self, wait: bool = True):
        self._running = False
        if wait:
            for t in self._workers:
                t.join()
        # daemon=True means threads die automatically if main process exits,
        # but join() is cleaner for graceful shutdown.


# ── Problem 3 ─────────────────────────────────────────────────────────────────
@dataclass(order=True)
class ScheduledTask:
    run_at: float
    task_id: str = field(compare=False)
    fn: callable = field(compare=False)


class Scheduler:
    def __init__(self):
        self._heap: list[ScheduledTask] = []

    def schedule(self, task_id: str, fn: callable, delay_seconds: float):
        task = ScheduledTask(run_at=time.time() + delay_seconds,
                             task_id=task_id, fn=fn)
        heapq.heappush(self._heap, task)

    def tick(self) -> list[str]:
        now = time.time()
        executed = []
        while self._heap and self._heap[0].run_at <= now:
            task = heapq.heappop(self._heap)
            task.fn()
            executed.append(task.task_id)
        return executed

    def pending_count(self) -> int:
        return len(self._heap)


# ── Interview talking points ───────────────────────────────────────────────────
"""
Q: How would you scale the WorkerPool to 1M concurrent agent executions?
A: The Python threading model is limited by the GIL for CPU-bound work.
   For I/O-bound (LLM API calls): asyncio + aiohttp gives much better concurrency.
   For true scale: push jobs to Kafka, workers are Kubernetes pods, each
   pod runs its own async worker. Redis tracks job state.
   This is exactly the architecture the Flowise team at Workday would use.

Q: Why heapq over a sorted list?
A: heapq.heappush/heappop are O(log n). Maintaining a sorted list is O(n).
   For a job queue processing thousands of jobs/sec, this matters.

Q: What's the difference between queue.Queue and collections.deque?
A: queue.Queue is thread-safe (has an internal lock). collections.deque is not.
   Use queue.Queue for producer-consumer between threads.
   Use deque for single-threaded FIFO (Phase 2 stacks/queues module).
"""

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
        print(f"  [{Priority(job.priority).name}] {job.job_id}")

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
    time.sleep(0.2)
    pool.stop()
    print(f"Processed {len(results)} jobs: {sorted(results)}")

    print("\n=== Scheduler ===")
    log = []
    sched = Scheduler()
    sched.schedule("task-a", lambda: log.append("a"), delay_seconds=0.0)
    sched.schedule("task-b", lambda: log.append("b"), delay_seconds=0.05)
    sched.schedule("task-c", lambda: log.append("c"), delay_seconds=10.0)

    ran = sched.tick()
    print(f"Ran immediately: {ran}")
    time.sleep(0.1)
    ran = sched.tick()
    print(f"Ran after 0.1s: {ran}")
    print(f"Still pending: {sched.pending_count()}")
