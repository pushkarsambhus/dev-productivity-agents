"""
SOLUTION: Phase 2 | Algorithms & DS | 04 Trees & Graphs
"""
from collections import deque
from dataclasses import dataclass, field


@dataclass
class TreeNode:
    val: int
    left: "TreeNode | None" = None
    right: "TreeNode | None" = None


def make_tree(values: list) -> TreeNode | None:
    if not values:
        return None
    root = TreeNode(values[0])
    queue = deque([root])
    i = 1
    while queue and i < len(values):
        node = queue.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
    return root


# ── Problem 1: BFS Level-Order ─────────────────────────────────────────────────
def level_order(root: TreeNode | None) -> list[list[int]]:
    if not root:
        return []
    result = []
    queue = deque([root])
    while queue:
        level_size = len(queue)          # snapshot: how many nodes at this level
        level = []
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level)
    return result
    # Key: snapshot len(queue) BEFORE processing a level.
    # This separates one level's nodes from the next level's nodes in the queue.


# ── Problem 2: DFS Max Depth ───────────────────────────────────────────────────
def max_depth(root: TreeNode | None) -> int:
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))
    # Base case: None node → depth 0
    # Recursive case: 1 (this node) + max depth of subtrees
    # This is the cleanest recursive formulation — memorize it.


# ── Problem 3: Graph BFS Shortest Path ────────────────────────────────────────
def shortest_path(graph: dict[str, list[str]], start: str, end: str) -> list[str]:
    if start == end:
        return [start]
    visited = {start}
    # Queue stores paths (not just nodes) so we can reconstruct the route
    queue = deque([[start]])
    while queue:
        path = queue.popleft()
        node = path[-1]
        for neighbor in graph.get(node, []):
            if neighbor == end:
                return path + [neighbor]
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])
    return []
    # BFS guarantees shortest path in an unweighted graph.
    # Storing full paths uses more memory than storing parent pointers,
    # but is cleaner for interview code. Mention the tradeoff.


# ── Problem 4: DFS Cycle Detection ────────────────────────────────────────────
def has_cycle(graph: dict[str, list[str]]) -> bool:
    visited = set()       # fully explored nodes
    in_path = set()       # nodes in the current DFS path

    def dfs(node: str) -> bool:
        in_path.add(node)
        visited.add(node)
        for neighbor in graph.get(node, []):
            if neighbor in in_path:       # back edge → cycle
                return True
            if neighbor not in visited:
                if dfs(neighbor):
                    return True
        in_path.remove(node)              # leaving this path
        return False

    return any(dfs(node) for node in graph if node not in visited)
    # Two sets are the key:
    # visited: prevents re-exploring nodes (efficiency)
    # in_path: detects back edges (cycle detection)
    # A back edge = we reached a node already in our current path = cycle


# ── Interview talking points ───────────────────────────────────────────────────
"""
BFS vs DFS — when to use which:
  BFS: shortest path, level-order, "closest" anything
  DFS: cycle detection, topological sort, path existence, tree structure

Complexity for both: O(V + E) time, O(V) space

Connection to your work:
  Level-order BFS → parallel execution tiers in a CI pipeline
  Cycle detection → validating a Flowise DAG before execution
  Shortest path → minimal dependency chain in build systems
"""

if __name__ == "__main__":
    tree = make_tree([3, 9, 20, None, None, 15, 7])
    print("=== Level Order ===")
    print(level_order(tree))
    print(level_order(None))

    print("\n=== Max Depth ===")
    print(max_depth(tree))
    print(max_depth(TreeNode(1)))

    print("\n=== Shortest Path ===")
    graph = {"a": ["b","c"], "b": ["d"], "c": ["d"], "d": ["e"], "e": []}
    print(shortest_path(graph, "a", "e"))
    print(shortest_path(graph, "a", "z"))

    print("\n=== Cycle Detection ===")
    print(has_cycle({"a": ["b"], "b": ["c"], "c": []}))   # False
    print(has_cycle({"a": ["b"], "b": ["c"], "c": ["a"]})) # True
