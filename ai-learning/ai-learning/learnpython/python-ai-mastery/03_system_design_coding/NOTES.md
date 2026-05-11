# Notes: System Design Coding Patterns

## heapq (Priority Queue)

```python
import heapq

heap = []
heapq.heappush(heap, (priority, item))   # O(log n)
heapq.heappop(heap)                       # O(log n) — returns smallest
heap[0]                                   # peek   — O(1)
heapq.heapify(list)                       # in-place — O(n)
heapq.nlargest(k, items, key=fn)          # top-k   — O(n log k)
heapq.nsmallest(k, items, key=fn)
```

**Python's heapq is a MIN-heap.** For max-heap: negate values, or use `(-priority, item)`.

For objects: use `@dataclass(order=True)` or implement `__lt__`.

---

## LRU Cache — Two Implementations

| | `OrderedDict` | Manual DLL + hashmap |
|---|---|---|
| Code | ~15 lines | ~40 lines |
| Interview signal | Knows stdlib | Understands the algorithm |
| When asked | "implement LRU" | "implement without OrderedDict" |

Always start with OrderedDict. Offer to explain the DLL version if asked.

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, cap):
        self.cap = cap
        self.cache = OrderedDict()

    def get(self, key):
        if key not in self.cache: return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, val):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = val
        if len(self.cache) > self.cap:
            self.cache.popitem(last=False)
```

---

## Rate Limiter Algorithms

| Algorithm | Pros | Cons |
|-----------|------|------|
| Token Bucket | Handles bursts, smooth | State per user |
| Fixed Window | Simple | Burst at window boundary |
| Sliding Window Log | Accurate | Memory-heavy |
| Sliding Window Counter | Memory-efficient | Approximate |

Token bucket is the standard answer for "design a rate limiter."

---

## Threading Primitives

```python
from threading import Thread, Lock, Event
import queue

# Thread-safe shared counter
lock = Lock()
with lock:
    counter += 1

# Worker pool pattern
q = queue.Queue()
def worker():
    while True:
        item = q.get(timeout=1.0)
        process(item)
        q.task_done()

threads = [Thread(target=worker, daemon=True) for _ in range(4)]
for t in threads: t.start()
```

---

## Design Pattern: Event-Driven Architecture

```
Publisher → Broker → [Subscriber1, Subscriber2, Subscriber3]
```

Decouples producers from consumers. Your LangChain build failure pipeline is event-driven:
- Event: "build failed" with log data
- Subscribers: classifier, alerter, audit logger

Production: replace in-memory broker with Kafka. API stays the same.

---

## Scaling from Prototype to Production

| Component | Prototype | Production |
|-----------|-----------|------------|
| Queue | `queue.Queue` | Kafka |
| Cache | `OrderedDict` | Redis |
| Rate limiter | In-memory dict | Redis atomic Lua script |
| Pub/sub | In-memory dict | Kafka topics |
| Scheduler | `heapq` + thread | Celery / APScheduler |

Know both levels — prototype shows you understand the algorithm, production shows you've shipped real systems.
