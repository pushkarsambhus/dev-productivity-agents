# Notes: Trees & Graphs

## BFS Template (level-order)

```python
from collections import deque

def bfs(root):
    if not root:
        return
    queue = deque([root])
    while queue:
        node = queue.popleft()
        # process node
        for neighbor in node.neighbors:   # or node.left, node.right for trees
            queue.append(neighbor)
```

**For level-by-level processing:**
```python
while queue:
    level_size = len(queue)          # snapshot BEFORE processing level
    for _ in range(level_size):
        node = queue.popleft()
        # process — all nodes here are the same level
        queue.append(node.left/right/neighbors...)
```

---

## DFS Templates

### Recursive (trees)
```python
def dfs(node):
    if not node:
        return base_case
    left  = dfs(node.left)
    right = dfs(node.right)
    return combine(left, right, node.val)
```

### Iterative (graphs)
```python
def dfs(graph, start):
    visited = set()
    stack = [start]
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        # process node
        stack.extend(graph[node])
```

---

## BFS vs DFS Decision Table

| Use BFS | Use DFS |
|---------|---------|
| Shortest path | Path exists (yes/no) |
| Level-by-level | Cycle detection |
| Closest node | Topological sort |
| "Fewest hops" | Tree structure (recursion natural) |

---

## Graph Representations

```python
# Adjacency list (most common in interviews)
graph = {
    "a": ["b", "c"],
    "b": ["d"],
    "c": [],
}

# Edge list → adjacency list
edges = [("a","b"), ("a","c"), ("b","d")]
from collections import defaultdict
adj = defaultdict(list)
for u, v in edges:
    adj[u].append(v)
```

---

## Cycle Detection Patterns

**Directed graph (DFS):** two sets — `visited` and `in_path`. Cycle if you reach a node in `in_path`.

**Undirected graph:** track parent. Cycle if you reach a visited node that isn't your parent.

**Topological sort (Kahn's):** cycle if not all nodes are processed (in_degree never reaches 0 for some). This is what your Phase 5 DAG scheduler detects.

---

## Interview Tip
Grid problems ("number of islands", "flood fill", "word search") are just graph problems in disguise. Each cell is a node, adjacent cells are edges. Apply BFS or DFS the same way. When you see a 2D grid — immediately think: "this is a graph."
