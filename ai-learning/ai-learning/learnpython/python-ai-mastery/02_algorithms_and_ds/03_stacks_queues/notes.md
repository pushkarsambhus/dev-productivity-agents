# Notes: Stacks & Queues

## Stack (LIFO)

```python
stack = []
stack.append(x)    # push  — O(1)
stack.pop()        # pop   — O(1)
stack[-1]          # peek  — O(1)
bool(stack)        # empty check
```

**When to use:** undo/redo, valid brackets, depth-first search, call stack simulation, "most recent" tracking.

---

## Queue (FIFO)

```python
from collections import deque
queue = deque()
queue.append(x)     # enqueue — O(1)
queue.popleft()     # dequeue — O(1)  ← use deque, NOT list.pop(0)
queue[0]            # peek    — O(1)
```

`list.pop(0)` is O(n) — it shifts all elements. Always use `deque` for queues.

**When to use:** BFS, task scheduling, sliding window (with maxlen), producer-consumer.

---

## Valid Brackets Template

```python
def is_valid(s):
    stack = []
    pairs = {")": "(", "]": "[", "}": "{"}
    for ch in s:
        if ch in "([{":
            stack.append(ch)
        elif ch in ")]}":
            if not stack or stack[-1] != pairs[ch]:
                return False
            stack.pop()
    return len(stack) == 0
```

Generalizes to: matching XML tags, validating nested JSON, parsing LLM tool calls.

---

## Monotonic Stack

A stack that maintains elements in sorted order. Used for "next greater element" problems.

```python
# Next greater element to the right:
result = [-1] * len(nums)
stack = []   # stores indices
for i, num in enumerate(nums):
    while stack and nums[stack[-1]] < num:
        idx = stack.pop()
        result[idx] = num   # num is the next greater for idx
    stack.append(i)
```

---

## Thread-Safe Queue

```python
import queue
q = queue.Queue()          # FIFO, thread-safe
q = queue.PriorityQueue()  # min-heap, thread-safe
q.put(item)
q.get(timeout=1.0)         # blocks, raises queue.Empty on timeout
q.task_done()              # signal processing complete
```

Use `queue.Queue` for multi-threaded producer-consumer. Use `deque` for single-threaded.

---

## Interview Tip
Stack problems often involve "matching" or "tracking state as you go." If you find yourself wanting to "undo" or "check the last thing you saw," reach for a stack. If you need to process things in the order they arrived, reach for a queue.
