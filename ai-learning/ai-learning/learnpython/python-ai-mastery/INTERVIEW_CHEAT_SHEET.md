# 🎯 Master Interview Cheat Sheet
## Principal / Staff Engineer — Python + AI/ML Systems

Read this the night before any interview.

---

## Part 1: Python Muscle Memory

### The Patterns You Must Write Without Thinking

```python
# ── Hashmap accumulate ──────────────────────────────────────────────────────
from collections import defaultdict, Counter
d = defaultdict(int)
d[key] += 1

counts = Counter(items)
counts.most_common(k)

# ── List/dict/set comprehension ─────────────────────────────────────────────
[x*2 for x in items if x > 0]
{k: v for k, v in d.items() if v > 0}
{x for x in items}   # set

# ── Flatten + deduplicate ───────────────────────────────────────────────────
unique = sorted(set(x for sub in nested for x in sub))

# ── Get first match lazily ──────────────────────────────────────────────────
first = next((x for x in items if condition(x)), None)

# ── Sort by multiple fields ─────────────────────────────────────────────────
items.sort(key=lambda x: (-x["score"], x["name"]))

# ── Enumerate + zip ─────────────────────────────────────────────────────────
for i, (a, b) in enumerate(zip(list1, list2)):
    ...

# ── Any / all ───────────────────────────────────────────────────────────────
has_failure = any(s < 0.7 for s in scores)
all_passing = all(s >= 0.8 for s in scores)

# ── Safe dict lookup ────────────────────────────────────────────────────────
val = d.get(key, default)
nested = d.get("outer", {}).get("inner", fallback)

# ── Swap without temp ───────────────────────────────────────────────────────
a, b = b, a

# ── Unpack ──────────────────────────────────────────────────────────────────
first, *middle, last = items
keys, vals = zip(*dict.items())

# ── Return bool directly (no if/else) ──────────────────────────────────────
return condition_a and condition_b
return not power_pellet_active and touching_ghost
```

---

## Part 2: Algorithm Templates

### Binary Search
```python
left, right = 0, len(arr) - 1
while left <= right:
    mid = left + (right - left) // 2
    if arr[mid] == target: return mid
    elif arr[mid] < target: left = mid + 1
    else: right = mid - 1
return -1
```

### Sliding Window (variable)
```python
left = 0
seen = set()
for right in range(len(arr)):
    while arr[right] in seen:
        seen.remove(arr[left]); left += 1
    seen.add(arr[right])
    best = max(best, right - left + 1)
```

### BFS
```python
from collections import deque
queue = deque([start])
visited = {start}
while queue:
    node = queue.popleft()
    for neighbor in graph[node]:
        if neighbor not in visited:
            visited.add(neighbor)
            queue.append(neighbor)
```

### DFS (recursive)
```python
def dfs(node):
    if not node: return 0
    return 1 + max(dfs(node.left), dfs(node.right))
```

### Topological Sort (Kahn's)
```python
from collections import deque, defaultdict
in_degree = {n: 0 for n in nodes}
adj = defaultdict(list)
for u, v in edges:
    adj[u].append(v); in_degree[v] += 1
queue = deque(n for n in nodes if in_degree[n] == 0)
order = []
while queue:
    n = queue.popleft(); order.append(n)
    for m in adj[n]:
        in_degree[m] -= 1
        if in_degree[m] == 0: queue.append(m)
if len(order) < len(nodes): raise ValueError("Cycle detected")
```

### Two Pointers
```python
left, right = 0, len(arr) - 1
while left < right:
    total = arr[left] + arr[right]
    if total == target: return [left, right]
    elif total < target: left += 1
    else: right -= 1
```

### LRU Cache (OrderedDict)
```python
from collections import OrderedDict
class LRUCache:
    def __init__(self, cap):
        self.cap = cap; self.cache = OrderedDict()
    def get(self, key):
        if key not in self.cache: return -1
        self.cache.move_to_end(key); return self.cache[key]
    def put(self, key, val):
        if key in self.cache: self.cache.move_to_end(key)
        self.cache[key] = val
        if len(self.cache) > self.cap: self.cache.popitem(last=False)
```

### Token Bucket Rate Limiter
```python
import time
class RateLimiter:
    def __init__(self, capacity, rate):
        self.capacity = capacity; self.tokens = capacity
        self.rate = rate; self.last = time.time()
    def allow(self):
        now = time.time()
        self.tokens = min(self.capacity, self.tokens + (now - self.last) * self.rate)
        self.last = now
        if self.tokens >= 1:
            self.tokens -= 1; return True
        return False
```

---

## Part 3: Complexity Reference

| Operation | List | Dict/Set | deque | heapq |
|-----------|------|----------|-------|-------|
| Access by index | O(1) | — | O(n) | — |
| Search | O(n) | O(1) | O(n) | O(n) |
| Insert at end | O(1) | O(1) | O(1) | O(log n) |
| Insert at front | O(n) | — | O(1) | — |
| Delete | O(n) | O(1) | O(1) ends | O(log n) |

---

## Part 4: AI/ML System Design Talking Points

### RAG Pipeline
- Chunk → Embed → Store → Retrieve → Augment → Generate
- Chunking: 256-512 tokens, 10-20% overlap
- Distance: cosine similarity on L2-normalized vectors
- Scale: ChromaDB (local) → Pinecone/pgvector (production), HNSW for ANN

### Agent Architectures
- ReAct: Reason → Act → Observe loop, max_steps safety valve
- Tool use: JSON structured output > text parsing in production
- Failure modes: hallucinated tool calls, context overflow, infinite loops
- Your work: smolagents CodeAgent, ReAct+FastAPI prototype

### Evals
- Answer Relevance, Faithfulness, Context Recall, Refusal Accuracy
- Your production work: LangSmith + DeepEval on build failure pipeline
- Adversarial: prompt injection, jailbreaks, data exfiltration, hallucination induction
- Datasets: HarmBench, AdvBench, TruthfulQA

### Observability
- Spans → Traces → Metrics → Alerts
- Key metrics: latency p50/p95/p99, token cost, error rate, cache hit rate
- Your story: 20-minute triage → near-instant (p50 improvement, 60+ teams)

### Scale (Flowise-style distributed system)
- Queue: Kafka for durable, partitioned job distribution
- Workers: Kubernetes pods, autoscale on queue depth
- State: Redis for job status, rate limiting, caching
- DAG execution: topological sort + priority queue, async parallel tiers

---

## Part 5: Your Principal-Level Stories

### Build Failure Detection Pipeline
**What:** Python/LangChain pipeline classifying CI failures → near-instant triage
**Metrics:** 20+ min → near-immediate, adopted by 60+ teams organically
**Stack:** LangChain, LangSmith, Python, Workday CI infrastructure
**Angle:** "I built the eval harness before the pipeline — TDD for LLMs"

### Platform Architecture at Scale
**What:** Technical strategy for 260+ engineers across 7 product areas
**Metrics:** CI/CD platform standards adopted organically by 60 teams
**Angle:** "I treat adoption like a product problem — solve the pain, standards follow"

### LLM Eval Prototype
**What:** LangSmith + DeepEval evaluation framework (prototype stage)
**What you can defend:** answer relevance, faithfulness, adversarial test cases
**Be honest about:** this is prototype/early-stage, not production-deployed

### ReAct Agent Prototype
**What:** smolagents CodeAgent + WebSearchTool, ReAct+FastAPI starter project
**What you can defend:** agent loop architecture, tool dispatch, failure modes
**Be honest about:** prototype for interview demonstration, not production-shipped

---

## Part 6: Questions to Ask Them

1. "How do you currently evaluate your LLM outputs in production — what metrics matter most to your team?"
2. "What does your AI red team / adversarial eval process look like today?"
3. "What's the biggest gap between your current eval coverage and what you'd want?"
4. "How are principal engineers involved in the ML platform vs. the product side?"
5. "What does a 6-month win look like for this role?"

---

## Part 7: The Night Before Checklist

- [ ] Re-read your top 3 stories (build failure, platform scale, eval prototype)
- [ ] Run through binary search template from memory
- [ ] Run through BFS template from memory
- [ ] Run through LRU cache from memory
- [ ] Review the role's JD — match their language to your language
- [ ] Sleep. Seriously.
