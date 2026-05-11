"""
PHASE 2 | ALGORITHMS & DS | 04 TREES & GRAPHS
==============================================
Topic: BFS, DFS, tree traversal. These underpin DAG execution engines,
dependency resolution, and knowledge graph traversal in AI systems.

You already implemented topological sort (Kahn's BFS) in Phase 5.
Here we build the foundation: BFS and DFS from scratch.
"""
from collections import deque
from dataclasses import dataclass, field


# ── Data structures ────────────────────────────────────────────────────────────
@dataclass
class TreeNode:
    val: int
    left: "TreeNode | None" = None
    right: "TreeNode | None" = None


def make_tree(values: list) -> TreeNode | None:
    """Build a binary tree from a level-order list (None = missing node)."""
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


# ── Problem 1: BFS Level-Order Traversal ──────────────────────────────────────
# Return the values of a binary tree level by level.
# Example tree [3,9,20,None,None,15,7]:
#       3
#      / \
#     9  20
#       /  \
#      15   7
# → [[3], [9, 20], [15, 7]]
# Use case: traversing a dependency graph level by level (parallel execution tiers)

def level_order(root: TreeNode | None) -> list[list[int]]:
    pass


# ── Problem 2: DFS — Max Depth ─────────────────────────────────────────────────
# Return the maximum depth (number of levels) of a binary tree.
# The tree above has depth 3.
# Recursion is the natural fit here.

def max_depth(root: TreeNode | None) -> int:
    pass


# ── Problem 3: Graph BFS — Shortest Path ──────────────────────────────────────
# Given an adjacency list graph and start/end nodes, return the
# shortest path (list of nodes) from start to end, or [] if unreachable.
#
# Use case: finding the minimal dependency chain in a build system.
#
# Example:
# graph = {"a": ["b","c"], "b": ["d"], "c": ["d"], "d": ["e"], "e": []}
# shortest_path(graph, "a", "e") → ["a", "b", "d", "e"]  (or via c — same length)

def shortest_path(graph: dict[str, list[str]], start: str, end: str) -> list[str]:
    pass


# ── Problem 4: DFS — Detect Cycle in Directed Graph ───────────────────────────
# Given a directed graph as adjacency list, return True if it contains a cycle.
# Use case: detecting circular dependencies in a task DAG (your Phase 5 problem
# used Kahn's algorithm; here we use DFS with a "currently visiting" set).
#
# A cycle exists if DFS reaches a node that's already in the current path.

def has_cycle(graph: dict[str, list[str]]) -> bool:
    pass


# ── Self-check ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    tree = make_tree([3, 9, 20, None, None, 15, 7])

    print("=== Level Order ===")
    print(level_order(tree))          # [[3], [9, 20], [15, 7]]
    print(level_order(None))          # []

    print("\n=== Max Depth ===")
    print(max_depth(tree))            # 3
    print(max_depth(TreeNode(1)))     # 1

    print("\n=== Shortest Path ===")
    graph = {"a": ["b","c"], "b": ["d"], "c": ["d"], "d": ["e"], "e": []}
    print(shortest_path(graph, "a", "e"))   # ['a', 'b', 'd', 'e'] or ['a', 'c', 'd', 'e']
    print(shortest_path(graph, "a", "z"))   # []

    print("\n=== Cycle Detection ===")
    acyclic = {"a": ["b"], "b": ["c"], "c": []}
    cyclic  = {"a": ["b"], "b": ["c"], "c": ["a"]}
    print(has_cycle(acyclic))   # False
    print(has_cycle(cyclic))    # True
