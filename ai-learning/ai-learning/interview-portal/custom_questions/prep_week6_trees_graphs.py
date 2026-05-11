"""
Coding Interview Prep — Week 6: DSA Trees & Graphs
===================================================
Covers: Linked Lists, Binary Trees (BFS/DFS), Binary Search Trees,
        Graphs BFS, Graphs DFS/Backtracking
"""

NAME        = "Week 6: Trees & Graphs"
DESCRIPTION = "Linked lists, binary trees, BST, BFS, DFS — pointer manipulation patterns"
ICON        = "🌳"

CONCEPTS = [
    {
        "title": "Linked Lists",
        "explanation": """A linked list is a sequence of nodes where each node holds a value and a pointer to the next node. No random access — must traverse from head.

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# Build: 1 → 2 → 3
head = ListNode(1, ListNode(2, ListNode(3)))
```

**Traversal:**
```python
curr = head
while curr:
    print(curr.val)
    curr = curr.next
```

**Three-pointer reverse (memorize):**
```python
prev, curr = None, head
while curr:
    next_node = curr.next   # 1. save next
    curr.next = prev        # 2. reverse pointer
    prev = curr             # 3. advance prev
    curr = next_node        # 4. advance curr
return prev   # new head
```

**Fast & slow pointers (detect cycle, find middle):**
```python
slow = fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
# slow is now at the middle
```""",
        "gotchas": [
            "Always save next_node before overwriting curr.next or you lose the rest of the list.",
            "Check for None before accessing .next to avoid AttributeError.",
            "head insert = O(1). Tail insert without tail pointer = O(n).",
        ],
        "videos": [
            {"title": "Linked Lists (NeetCode)", "url": "https://www.youtube.com/watch?v=G0_I-ZF0S38", "source": "YouTube"},
            {"title": "Reverse Linked List (NeetCode)", "url": "https://www.youtube.com/watch?v=G0_I-ZF0S38", "source": "YouTube"},
            {"title": "Master the Coding Interview — Linked Lists", "url": "https://www.udemy.com/course/master-the-coding-interview-data-structures-algorithms/", "source": "Udemy"},
        ],
    },
    {
        "title": "Binary Trees — DFS & BFS",
        "explanation": """**Binary tree node:**
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

**DFS traversals (recursive):**
```python
def inorder(root):    # Left → Root → Right (sorted on BST)
    if not root: return []
    return inorder(root.left) + [root.val] + inorder(root.right)

def preorder(root):   # Root → Left → Right
    if not root: return []
    return [root.val] + preorder(root.left) + preorder(root.right)
```

**DFS template (most tree problems):**
```python
def solve(root):
    if not root: return BASE_CASE
    left = solve(root.left)
    right = solve(root.right)
    return COMBINE(left, right, root.val)
```

**BFS (level-order) — use deque:**
```python
from collections import deque
def level_order(root):
    if not root: return []
    result, queue = [], deque([root])
    while queue:
        level_size = len(queue)   # snapshot — critical!
        level = []
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            if node.left:  queue.append(node.left)
            if node.right: queue.append(node.right)
        result.append(level)
    return result
```""",
        "gotchas": [
            "DFS base case: if not root: return 0 (or [] or None depending on problem).",
            "BFS: snapshot len(queue) BEFORE the inner loop — this separates levels.",
            "In-order on BST = sorted output. Always.",
            "Use deque for BFS — list.pop(0) is O(n).",
        ],
        "videos": [
            {"title": "Binary Tree Algorithms (freeCodeCamp)", "url": "https://www.youtube.com/watch?v=fAAZixBzIAI", "source": "YouTube"},
            {"title": "BFS vs DFS for Trees (NeetCode)", "url": "https://www.youtube.com/watch?v=OnSn2XEQ4MY", "source": "YouTube"},
            {"title": "Master the Coding Interview — Trees", "url": "https://www.udemy.com/course/master-the-coding-interview-data-structures-algorithms/", "source": "Udemy"},
        ],
    },
    {
        "title": "Graphs — BFS & DFS",
        "explanation": """Graphs = nodes (vertices) + edges. Can be directed/undirected, weighted/unweighted, cyclic/acyclic.

**Representation:**
```python
# Adjacency list (most common in interviews)
graph = {
    0: [1, 2],
    1: [0, 3],
    2: [0, 3],
    3: [1, 2],
}
```

**BFS — shortest path in unweighted graph:**
```python
from collections import deque
def bfs(graph, start, end):
    visited = {start}
    queue = deque([(start, 0)])
    while queue:
        node, dist = queue.popleft()
        if node == end: return dist
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)   # mark WHEN enqueuing
                queue.append((neighbor, dist + 1))
    return -1
```

**DFS — flood fill, connected components:**
```python
def dfs(graph, node, visited):
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
```

**Number of islands = flood fill:**
```python
def dfs(grid, r, c):
    if r < 0 or r >= len(grid) or c < 0 or c >= len(grid[0]) or grid[r][c] != '1':
        return
    grid[r][c] = '0'   # mark visited in-place
    for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
        dfs(grid, r+dr, c+dc)
```""",
        "gotchas": [
            "Mark nodes visited WHEN ENQUEUING in BFS — not when dequeuing. Prevents duplicates.",
            "Always use a visited set in graphs — unlike trees, graphs can have cycles.",
            "BFS = shortest path (unweighted). DFS = connectivity, flood fill, backtracking.",
        ],
        "videos": [
            {"title": "Graph Algorithms (freeCodeCamp)", "url": "https://www.youtube.com/watch?v=tWVWeAqZ0WU", "source": "YouTube"},
            {"title": "BFS & DFS Graph (NeetCode)", "url": "https://www.youtube.com/watch?v=oDqjPvD1Uzg", "source": "YouTube"},
            {"title": "Master the Coding Interview — Graphs", "url": "https://www.udemy.com/course/master-the-coding-interview-data-structures-algorithms/", "source": "Udemy"},
        ],
    },
]

QUESTIONS = [

    # ══════════════════════════════════════════════════════════════════
    # LINKED LISTS
    # ══════════════════════════════════════════════════════════════════
    {
        "type": "mcq",
        "difficulty": "easy",
        "topic": "Linked Lists",
        "question": (
            "What is the time complexity of inserting a node at the HEAD of a singly linked list?"
        ),
        "options": [
            "A) O(n) — must traverse to find the end",
            "B) O(1) — just update the head pointer",
            "C) O(log n) — binary search for position",
            "D) O(n²) — shifting elements",
        ],
        "correct_answer": "B) O(1) — just update the head pointer",
        "explanation": (
            "Inserting at the head of a linked list is O(1): create new node, set new_node.next = head, "
            "update head = new_node. No traversal needed. "
            "Contrast with inserting at the TAIL (O(n) without a tail pointer) or in the MIDDLE (O(n)). "
            "Contrast with ArrayList in Java: insert at beginning is O(n) due to element shifting. "
            "This is a key advantage of linked lists over arrays for head insertions."
        ),
        "remember": "Linked list head insert = O(1). Array insert at beginning = O(n). Trade-off: no random access in linked lists.",
    },
    {
        "type": "coding",
        "difficulty": "medium",
        "topic": "Linked Lists",
        "question": (
            "Reverse a singly linked list in-place. Return the new head.\n\n"
            "The ListNode class is provided. Implement reverse_list.\n\n"
            "Example:\n"
            "  Input:  1 → 2 → 3 → 4 → None\n"
            "  Output: 4 → 3 → 2 → 1 → None"
        ),
        "language": "python",
        "starter_code": (
            "class ListNode:\n"
            "    def __init__(self, val=0, next=None):\n"
            "        self.val = val\n"
            "        self.next = next\n\n\n"
            "def reverse_list(head: ListNode) -> ListNode:\n"
            "    pass\n"
        ),
        "correct_answer": (
            "def reverse_list(head: ListNode) -> ListNode:\n"
            "    prev = None\n"
            "    curr = head\n"
            "    while curr:\n"
            "        next_node = curr.next   # save next\n"
            "        curr.next = prev        # reverse pointer\n"
            "        prev = curr             # advance prev\n"
            "        curr = next_node        # advance curr\n"
            "    return prev\n"
        ),
        "explanation": (
            "Three-pointer technique: prev, curr, next_node. "
            "Save next_node before overwriting curr.next. Reverse the pointer. Advance both prev and curr. "
            "After the loop, prev is the new head (curr is None). "
            "O(n) time, O(1) space — no extra data structures. "
            "This is the most commonly asked linked list question. Know it cold."
        ),
        "remember": "Reverse linked list: save next, flip pointer, advance both. O(n) time O(1) space. Three pointers.",
    },

    # ══════════════════════════════════════════════════════════════════
    # BINARY TREES
    # ══════════════════════════════════════════════════════════════════
    {
        "type": "mcq",
        "difficulty": "easy",
        "topic": "Binary Trees",
        "question": (
            "Which traversal visits nodes in the order: left subtree → root → right subtree?"
        ),
        "options": [
            "A) Pre-order",
            "B) In-order",
            "C) Post-order",
            "D) Level-order (BFS)",
        ],
        "correct_answer": "B) In-order",
        "explanation": (
            "In-order: Left → Root → Right. On a BST, this produces sorted output. "
            "Pre-order: Root → Left → Right (useful for copying a tree). "
            "Post-order: Left → Right → Root (useful for deleting a tree). "
            "Level-order: BFS using a queue, visits nodes level by level. "
            "In interviews, in-order is most commonly asked for BSTs."
        ),
        "remember": "In-order = Left→Root→Right = sorted output on BST. Pre = Root first. Post = Root last. Level = BFS.",
    },
    {
        "type": "coding",
        "difficulty": "medium",
        "topic": "Binary Trees — DFS",
        "question": (
            "Find the maximum depth (height) of a binary tree using recursion.\n\n"
            "The TreeNode class is provided.\n\n"
            "Examples:\n"
            "      3\n"
            "     / \\\n"
            "    9  20\n"
            "       / \\\n"
            "      15   7\n\n"
            "  max_depth(root) → 3"
        ),
        "language": "python",
        "starter_code": (
            "class TreeNode:\n"
            "    def __init__(self, val=0, left=None, right=None):\n"
            "        self.val = val\n"
            "        self.left = left\n"
            "        self.right = right\n\n\n"
            "def max_depth(root: TreeNode) -> int:\n"
            "    pass\n"
        ),
        "correct_answer": (
            "def max_depth(root: TreeNode) -> int:\n"
            "    if root is None:\n"
            "        return 0\n"
            "    return 1 + max(max_depth(root.left), max_depth(root.right))\n"
        ),
        "explanation": (
            "Classic DFS recursion on trees. Base case: None → depth 0. "
            "Recursive case: 1 (for current node) + max of left and right subtree depths. "
            "O(n) time (visits every node), O(h) space (call stack = tree height h, "
            "O(log n) for balanced, O(n) worst case for skewed tree). "
            "This pattern — recurse left, recurse right, combine — appears in most tree problems."
        ),
        "remember": "Tree DFS template: if not root: return base. return combine(recurse(left), recurse(right)).",
    },
    {
        "type": "coding",
        "difficulty": "medium",
        "topic": "Binary Trees — BFS",
        "question": (
            "Return the level-order traversal of a binary tree as a list of lists.\n\n"
            "Example:\n"
            "      3\n"
            "     / \\\n"
            "    9  20\n"
            "       / \\\n"
            "      15   7\n\n"
            "  level_order(root) → [[3], [9, 20], [15, 7]]"
        ),
        "language": "python",
        "starter_code": (
            "from collections import deque\n\n\n"
            "class TreeNode:\n"
            "    def __init__(self, val=0, left=None, right=None):\n"
            "        self.val = val\n"
            "        self.left = left\n"
            "        self.right = right\n\n\n"
            "def level_order(root: TreeNode) -> list:\n"
            "    pass\n"
        ),
        "correct_answer": (
            "def level_order(root: TreeNode) -> list:\n"
            "    if not root:\n"
            "        return []\n"
            "    result = []\n"
            "    queue = deque([root])\n"
            "    while queue:\n"
            "        level_size = len(queue)\n"
            "        level = []\n"
            "        for _ in range(level_size):\n"
            "            node = queue.popleft()\n"
            "            level.append(node.val)\n"
            "            if node.left:\n"
            "                queue.append(node.left)\n"
            "            if node.right:\n"
            "                queue.append(node.right)\n"
            "        result.append(level)\n"
            "    return result\n"
        ),
        "explanation": (
            "BFS uses a queue (deque for O(1) popleft). "
            "The key insight for level separation: snapshot the queue size at the start of each level. "
            "Process exactly that many nodes — those are all at the same level. "
            "Then add their children (next level) to the queue. "
            "Use collections.deque, not list, for the queue — list.pop(0) is O(n), deque.popleft() is O(1). "
            "Trigger: process nodes level by level, find level of a node, connect next right pointers."
        ),
        "remember": "BFS template: deque + while queue + snapshot level_size + inner loop. Always use deque not list for queue.",
    },

    # ══════════════════════════════════════════════════════════════════
    # BINARY SEARCH TREES
    # ══════════════════════════════════════════════════════════════════
    {
        "type": "mcq",
        "difficulty": "medium",
        "topic": "Binary Search Trees",
        "question": (
            "What is the time complexity of search in a balanced BST vs a degenerate (skewed) BST?"
        ),
        "options": [
            "A) O(log n) for both",
            "B) O(log n) for balanced, O(n) for degenerate",
            "C) O(n) for both",
            "D) O(1) for balanced, O(log n) for degenerate",
        ],
        "correct_answer": "B) O(log n) for balanced, O(n) for degenerate",
        "explanation": (
            "A balanced BST has height O(log n) — each comparison halves the search space. "
            "A degenerate BST (all nodes inserted in sorted order) degenerates into a linked list "
            "with height O(n). This is why self-balancing BSTs (AVL, Red-Black) exist. "
            "Java's TreeMap uses Red-Black tree — always O(log n). "
            "This is a key interview concept: BST advantage disappears without balancing."
        ),
        "remember": "BST search: O(log n) balanced, O(n) skewed. Worst case = sorted insertion = linked list.",
    },

    # ══════════════════════════════════════════════════════════════════
    # GRAPHS
    # ══════════════════════════════════════════════════════════════════
    {
        "type": "coding",
        "difficulty": "hard",
        "topic": "Graphs — BFS",
        "question": (
            "Given a graph as an adjacency list and two nodes, return the shortest path length "
            "between them (number of edges). Return -1 if no path exists.\n\n"
            "Example:\n"
            "  graph = {0:[1,2], 1:[0,3], 2:[0,3], 3:[1,2,4], 4:[3]}\n"
            "  shortest_path(graph, 0, 4) → 3  (0→1→3→4 or 0→2→3→4)"
        ),
        "language": "python",
        "starter_code": (
            "from collections import deque\n\n\n"
            "def shortest_path(graph: dict, start: int, end: int) -> int:\n"
            "    pass\n"
        ),
        "correct_answer": (
            "def shortest_path(graph: dict, start: int, end: int) -> int:\n"
            "    if start == end:\n"
            "        return 0\n"
            "    visited = {start}\n"
            "    queue = deque([(start, 0)])\n"
            "    while queue:\n"
            "        node, dist = queue.popleft()\n"
            "        for neighbor in graph[node]:\n"
            "            if neighbor == end:\n"
            "                return dist + 1\n"
            "            if neighbor not in visited:\n"
            "                visited.add(neighbor)\n"
            "                queue.append((neighbor, dist + 1))\n"
            "    return -1\n"
        ),
        "explanation": (
            "BFS guarantees shortest path in an unweighted graph — it explores level by level. "
            "The visited set prevents infinite loops in cyclic graphs. "
            "Mark nodes visited WHEN ENQUEUED (not when dequeued) to avoid re-adding them. "
            "O(V + E) time and space where V = vertices, E = edges. "
            "For weighted shortest path, use Dijkstra's algorithm instead."
        ),
        "remember": "BFS = shortest path in unweighted graph. Mark visited when enqueuing, not dequeuing. O(V+E).",
    },
    {
        "type": "coding",
        "difficulty": "hard",
        "topic": "Graphs — DFS / Backtracking",
        "question": (
            "Given an m x n grid of '1' (land) and '0' (water), count the number of islands.\n"
            "An island is surrounded by water and formed by connecting adjacent land cells horizontally or vertically.\n\n"
            "Example:\n"
            "  grid = [\n"
            "    ['1','1','0','0'],\n"
            "    ['1','1','0','1'],\n"
            "    ['0','0','0','1'],\n"
            "  ]\n"
            "  num_islands(grid) → 2"
        ),
        "language": "python",
        "starter_code": (
            "def num_islands(grid: list) -> int:\n"
            "    pass\n"
        ),
        "correct_answer": (
            "def num_islands(grid: list) -> int:\n"
            "    if not grid:\n"
            "        return 0\n"
            "    rows, cols = len(grid), len(grid[0])\n"
            "    count = 0\n\n"
            "    def dfs(r, c):\n"
            "        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != '1':\n"
            "            return\n"
            "        grid[r][c] = '0'   # mark visited\n"
            "        dfs(r+1, c)\n"
            "        dfs(r-1, c)\n"
            "        dfs(r, c+1)\n"
            "        dfs(r, c-1)\n\n"
            "    for r in range(rows):\n"
            "        for c in range(cols):\n"
            "            if grid[r][c] == '1':\n"
            "                count += 1\n"
            "                dfs(r, c)\n"
            "    return count\n"
        ),
        "explanation": (
            "Classic DFS flood-fill. For each unvisited '1', increment count and DFS to sink the entire island "
            "(mark all connected '1' cells as '0' = visited). "
            "The next unvisited '1' we find must be a new island. "
            "O(m*n) time and space. Modifying the grid in-place avoids a visited matrix. "
            "If you can't modify the grid, use a visited set of (r,c) tuples."
        ),
        "remember": "Number of islands = flood fill. DFS/BFS from each unvisited '1', mark visited. Count triggers = island count.",
    },
]
