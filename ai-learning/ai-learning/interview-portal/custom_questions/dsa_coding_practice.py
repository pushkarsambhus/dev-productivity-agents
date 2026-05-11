"""
DSA, Python & AI Agents — Coding Practice Pack
================================================
Covers: Python fundamentals, DSA patterns, and AI Agents concepts.
Ordered easy → hard within each tier.
"""

NAME        = "DSA, Python & AI Agents"
DESCRIPTION = "Data structures, algorithms, Python internals, and AI agent patterns — interview-focused"
ICON        = "🧠"

QUESTIONS = [

    # ══════════════════════════════════════════════════════════════════════════
    # EASY
    # ══════════════════════════════════════════════════════════════════════════

    {
        "type": "mcq",
        "difficulty": "easy",
        "topic": "Python — list vs tuple",
        "question": (
            "Which statement correctly describes the key difference between a Python "
            "list and a tuple?"
        ),
        "options": [
            "A) Lists are ordered; tuples are unordered",
            "B) Lists are mutable; tuples are immutable",
            "C) Lists allow duplicate values; tuples do not",
            "D) Lists use less memory than tuples for the same data",
        ],
        "correct_answer": "B) Lists are mutable; tuples are immutable",
        "explanation": (
            "The defining difference is mutability. You can append, remove, or reassign "
            "elements in a list. Tuples are fixed after creation — you cannot change their "
            "contents. Both are ordered and allow duplicates. Tuples actually use slightly "
            "less memory because they have no over-allocation overhead."
        ),
        "remember": "list = mutable, tuple = immutable. Tuples are slightly faster and hashable (can be dict keys).",
    },
    {
        "type": "mcq",
        "difficulty": "easy",
        "topic": "Python — dictionary lookup complexity",
        "question": "What is the average-case time complexity of a key lookup in a Python dict?",
        "options": [
            "A) O(log n)",
            "B) O(n)",
            "C) O(1)",
            "D) O(n log n)",
        ],
        "correct_answer": "C) O(1)",
        "explanation": (
            "Python dicts are hash tables. A key lookup computes the hash of the key "
            "(O(1)), then probes the internal array at that index. Collisions can cause "
            "worst-case O(n), but with a good hash function and Python's randomised hashing "
            "this is virtually never seen in practice."
        ),
        "remember": "dict/set lookup: O(1) average, O(n) worst case. Same for insert and delete.",
    },
    {
        "type": "mcq",
        "difficulty": "easy",
        "topic": "DSA — Big-O notation",
        "question": (
            "A function iterates over an array of n elements, and for each element "
            "calls a helper that also iterates over all n elements. What is the overall "
            "time complexity?"
        ),
        "options": [
            "A) O(n)",
            "B) O(n log n)",
            "C) O(n²)",
            "D) O(2n)",
        ],
        "correct_answer": "C) O(n²)",
        "explanation": (
            "Two nested loops each running n iterations give n × n = n² operations. "
            "O(2n) is not a standard notation — constants are dropped in Big-O. "
            "This nested-loop pattern is the classic signature of O(n²) algorithms "
            "like bubble sort or checking all pairs in an array."
        ),
        "remember": "Nested loop over same n → O(n²). Triple nested → O(n³). Spot this pattern immediately.",
    },
    {
        "type": "mcq",
        "difficulty": "easy",
        "topic": "Python — `is` vs `==`",
        "question": (
            "What is the difference between `is` and `==` in Python?\n\n"
            "a = [1, 2, 3]\n"
            "b = [1, 2, 3]\n"
            "print(a == b)  # ?\n"
            "print(a is b)  # ?"
        ),
        "options": [
            "A) Both print True because lists with same content are identical",
            "B) `==` prints True (same value); `is` prints False (different objects)",
            "C) `==` prints False; `is` prints True",
            "D) Both print False because lists are mutable",
        ],
        "correct_answer": "B) `==` prints True (same value); `is` prints False (different objects)",
        "explanation": (
            "`==` compares values (calls __eq__). `is` checks object identity — whether "
            "both variables point to the exact same object in memory. Two list literals "
            "with identical contents are different objects, so `is` is False. Python "
            "caches small integers (-5 to 256) and interned strings, which can make `is` "
            "return True unexpectedly — never rely on `is` for value comparison."
        ),
        "remember": "`is` = same object (identity). `==` = same value. Never use `is` to compare strings or numbers you didn't intern.",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # MEDIUM
    # ══════════════════════════════════════════════════════════════════════════

    {
        "type": "find_the_bug",
        "difficulty": "medium",
        "topic": "Python — mutable default argument",
        "question": "Find and fix the bug in this Python function:",
        "language": "python",
        "code": (
            "def append_to(element, target=[]):\n"
            "    target.append(element)\n"
            "    return target\n"
            "\n"
            "print(append_to(1))  # Expected: [1]\n"
            "print(append_to(2))  # Expected: [2]  — got: [1, 2] !"
        ),
        "correct_answer": (
            "The default argument `target=[]` is evaluated ONCE when the function is "
            "defined, not each time it is called. The same list object is reused across "
            "calls. Fix: use `None` as the default and create a new list inside the body.\n\n"
            "def append_to(element, target=None):\n"
            "    if target is None:\n"
            "        target = []\n"
            "    target.append(element)\n"
            "    return target"
        ),
        "explanation": (
            "Python evaluates default argument values at function definition time, not "
            "at call time. Mutable defaults (list, dict, set) persist across calls and "
            "accumulate state. The canonical fix is to use a sentinel (None) and "
            "initialise the mutable inside the body. This is one of the top Python "
            "interview gotchas."
        ),
        "remember": "Never use mutable objects ([], {}, set()) as default arguments. Use None and initialise inside the function.",
    },
    {
        "type": "coding",
        "difficulty": "medium",
        "topic": "DSA — Two-pointer / sliding window",
        "question": (
            "Given a list of integers `nums` and an integer `k`, return the maximum sum "
            "of any contiguous subarray of length exactly `k`.\n\n"
            "Examples:\n"
            "  max_subarray_sum([2, 1, 5, 1, 3, 2], k=3)  →  9  (subarray [5,1,3])\n"
            "  max_subarray_sum([2, 3, 4, 1, 5], k=2)     →  7  (subarray [3,4])\n\n"
            "Solve in O(n) time."
        ),
        "language": "python",
        "starter_code": (
            "from typing import List\n\n\n"
            "def max_subarray_sum(nums: List[int], k: int) -> int:\n"
            '    """\n'
            "    Return the maximum sum of any contiguous subarray of length k.\n"
            "    Time: O(n), Space: O(1)\n"
            '    """\n'
            "    pass\n"
        ),
        "correct_answer": (
            "def max_subarray_sum(nums, k):\n"
            "    window = sum(nums[:k])\n"
            "    best = window\n"
            "    for i in range(k, len(nums)):\n"
            "        window += nums[i] - nums[i - k]\n"
            "        best = max(best, window)\n"
            "    return best\n"
        ),
        "explanation": (
            "Sliding window pattern: compute the sum of the first window of size k, then "
            "slide one step at a time by adding the new element entering the window and "
            "subtracting the one leaving. This avoids recomputing the sum from scratch on "
            "every step, giving O(n) overall vs O(n*k) for the naive approach."
        ),
        "remember": "Fixed-size window → slide by adding right element and removing left element. O(n) instead of O(n*k).",
    },
    {
        "type": "coding",
        "difficulty": "medium",
        "topic": "DSA — HashMap / frequency count",
        "question": (
            "Given a string `s`, find the first non-repeating character and return its "
            "index. If no such character exists, return -1.\n\n"
            "Examples:\n"
            "  first_unique_char('leetcode')   →  0  ('l')\n"
            "  first_unique_char('loveleetcode') →  2  ('v')\n"
            "  first_unique_char('aabb')        →  -1\n\n"
            "Solve in O(n) time."
        ),
        "language": "python",
        "starter_code": (
            "def first_unique_char(s: str) -> int:\n"
            '    """\n'
            "    Return index of first character that appears exactly once.\n"
            "    Return -1 if none exists.\n"
            '    """\n'
            "    pass\n"
        ),
        "correct_answer": (
            "from collections import Counter\n\n"
            "def first_unique_char(s):\n"
            "    count = Counter(s)\n"
            "    for i, ch in enumerate(s):\n"
            "        if count[ch] == 1:\n"
            "            return i\n"
            "    return -1\n"
        ),
        "explanation": (
            "Two-pass O(n) approach: first build a frequency map (Counter or dict), then "
            "iterate the string a second time and return the index of the first character "
            "with count == 1. Total: O(n) time, O(1) space (alphabet is bounded at 26)."
        ),
        "remember": "Frequency problems → Counter/dict first pass, then find in second pass. Classic hashmap pattern.",
    },
    {
        "type": "mcq",
        "difficulty": "medium",
        "topic": "DSA — Stack",
        "question": (
            "You need to validate that brackets in a string are correctly nested and "
            "closed. E.g. '([{}])' is valid, '([)]' is not. Which data structure is "
            "most naturally suited for this problem and why?"
        ),
        "options": [
            "A) Queue — because we process characters in the order they appear",
            "B) Stack — because we need to match the most recently opened bracket first (LIFO)",
            "C) Hash map — because we need to look up the matching bracket in O(1)",
            "D) Heap — because we need to prioritise closing brackets over opening ones",
        ],
        "correct_answer": "B) Stack — because we need to match the most recently opened bracket first (LIFO)",
        "explanation": (
            "Bracket matching requires LIFO (Last In, First Out) semantics: the last "
            "opening bracket must be closed first. A stack lets you push opening brackets "
            "and pop when you see a closing one — if the popped bracket matches, continue; "
            "otherwise the string is invalid. A hash map is a helpful companion (to store "
            "the matching pair) but the core data structure is the stack."
        ),
        "remember": "Nested structure problems (brackets, call stacks, undo history) → think Stack (LIFO) first.",
    },
    {
        "type": "mcq",
        "difficulty": "medium",
        "topic": "AI Agents — Tool use",
        "question": (
            "In an LLM-based agent architecture, what is the purpose of 'tool use' "
            "(also called function calling)?"
        ),
        "options": [
            "A) It allows the LLM to modify its own weights during inference",
            "B) It lets the LLM request execution of external functions and receive their results, extending what it can do beyond text generation",
            "C) It caches common LLM outputs to reduce API costs",
            "D) It enables the LLM to run Python code entirely inside its context window",
        ],
        "correct_answer": (
            "B) It lets the LLM request execution of external functions and receive their results, "
            "extending what it can do beyond text generation"
        ),
        "explanation": (
            "Tool use (function calling) is the mechanism by which an LLM signals that it "
            "wants to call a specific function with specific arguments. The host application "
            "executes the function and feeds the result back to the model. This lets the "
            "model perform actions like web search, database queries, code execution, or API "
            "calls — things it cannot do natively with text generation alone."
        ),
        "remember": "Tool use = LLM requests function → host executes → result fed back. The model never executes code itself.",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # HARD
    # ══════════════════════════════════════════════════════════════════════════

    {
        "type": "coding",
        "difficulty": "hard",
        "topic": "DSA — Binary search",
        "question": (
            "Given a sorted array of distinct integers `nums` and a target integer, "
            "return the index of the target. If not found, return the index where it "
            "would be inserted to keep the array sorted.\n\n"
            "You MUST solve this in O(log n) time — no linear scan.\n\n"
            "Examples:\n"
            "  search_insert([1,3,5,6], 5)  →  2\n"
            "  search_insert([1,3,5,6], 2)  →  1\n"
            "  search_insert([1,3,5,6], 7)  →  4\n"
            "  search_insert([1,3,5,6], 0)  →  0"
        ),
        "language": "python",
        "starter_code": (
            "from typing import List\n\n\n"
            "def search_insert(nums: List[int], target: int) -> int:\n"
            '    """\n'
            "    Return index of target, or insertion index if not found.\n"
            "    Time: O(log n)\n"
            '    """\n'
            "    pass\n"
        ),
        "correct_answer": (
            "def search_insert(nums, target):\n"
            "    lo, hi = 0, len(nums) - 1\n"
            "    while lo <= hi:\n"
            "        mid = (lo + hi) // 2\n"
            "        if nums[mid] == target:\n"
            "            return mid\n"
            "        elif nums[mid] < target:\n"
            "            lo = mid + 1\n"
            "        else:\n"
            "            hi = mid - 1\n"
            "    return lo  # lo is the insertion point when not found\n"
        ),
        "explanation": (
            "Standard binary search with a small twist: when the target is not found, "
            "the `lo` pointer ends up at the first position where all elements to the "
            "left are smaller than the target — exactly the insertion point. Key insight: "
            "after the loop, lo > hi and lo points to where target should go."
        ),
        "remember": "Binary search on sorted array: O(log n). After loop, `lo` = correct insertion index. Know this cold.",
    },
    {
        "type": "coding",
        "difficulty": "hard",
        "topic": "DSA — Recursion / Dynamic programming",
        "question": (
            "Implement Fibonacci with memoization (top-down DP).\n\n"
            "fib(0) = 0, fib(1) = 1, fib(n) = fib(n-1) + fib(n-2)\n\n"
            "Examples:\n"
            "  fib(0)  →  0\n"
            "  fib(1)  →  1\n"
            "  fib(6)  →  8\n"
            "  fib(10) →  55\n\n"
            "Plain recursion is O(2^n) — memoize to bring it to O(n)."
        ),
        "language": "python",
        "starter_code": (
            "def fib(n: int, memo: dict = None) -> int:\n"
            '    """\n'
            "    Return the nth Fibonacci number using memoization.\n"
            "    Time: O(n), Space: O(n)\n"
            '    """\n'
            "    pass\n"
        ),
        "correct_answer": (
            "def fib(n, memo=None):\n"
            "    if memo is None:\n"
            "        memo = {}\n"
            "    if n <= 1:\n"
            "        return n\n"
            "    if n in memo:\n"
            "        return memo[n]\n"
            "    memo[n] = fib(n - 1, memo) + fib(n - 2, memo)\n"
            "    return memo[n]\n"
            "\n"
            "# Alternatively, use @functools.lru_cache(maxsize=None)\n"
        ),
        "explanation": (
            "Without memoization, the recursion tree has exponential branches — fib(n) "
            "is called twice at each level, giving O(2^n). With a memo dict, each value "
            "is computed only once and cached. Subsequent calls hit the cache in O(1). "
            "Total: O(n) time and O(n) space for the memo. The iterative bottom-up "
            "approach achieves O(1) space if you only keep the last two values."
        ),
        "remember": "Memoization = cache + recursion = top-down DP. Use a dict or @lru_cache. Turns O(2^n) → O(n) for Fibonacci.",
    },
    {
        "type": "find_the_bug",
        "difficulty": "hard",
        "topic": "DSA — BFS / graph traversal",
        "question": "Find and fix the bug in this BFS shortest-path implementation:",
        "language": "python",
        "code": (
            "from collections import deque\n"
            "\n"
            "def bfs_shortest(graph: dict, start: str, end: str) -> int:\n"
            "    \"\"\"Return the number of edges in the shortest path from start to end.\"\"\"\n"
            "    queue = deque([(start, 0)])\n"
            "    visited = set()\n"
            "    while queue:\n"
            "        node, dist = queue.popleft()\n"
            "        if node == end:\n"
            "            return dist\n"
            "        for neighbor in graph.get(node, []):\n"
            "            if neighbor not in visited:\n"
            "                visited.add(neighbor)\n"
            "                queue.append((neighbor, dist + 1))\n"
            "    return -1"
        ),
        "correct_answer": (
            "The bug: `start` is never added to `visited` before the loop begins. "
            "If graph contains a cycle back to `start`, the start node will be enqueued "
            "again, leading to duplicate processing and potentially an incorrect answer "
            "or infinite loop.\n\n"
            "Fix: add `visited.add(start)` before the while loop (or right after "
            "creating the set):\n\n"
            "    visited = set()\n"
            "    visited.add(start)   # <-- add this line\n"
            "    queue = deque([(start, 0)])"
        ),
        "explanation": (
            "In BFS, a node should be marked visited when it is added to the queue, not "
            "when it is dequeued. Marking on dequeue means a node can be added to the "
            "queue multiple times before being processed. The start node must be marked "
            "immediately, otherwise any back-edge pointing to `start` will re-enqueue it. "
            "This is a classic BFS bug that causes both incorrect answers and, in dense "
            "graphs, O(n²) performance instead of O(V+E)."
        ),
        "remember": "BFS: mark visited WHEN you enqueue (not dequeue). Always add start to visited before the loop.",
    },
    {
        "type": "mcq",
        "difficulty": "hard",
        "topic": "AI Agents — ReAct pattern",
        "question": (
            "In the ReAct (Reasoning + Acting) agent pattern, what is the purpose of "
            "the 'Thought' step that precedes each 'Action'?"
        ),
        "options": [
            "A) It stores the action result in long-term memory for future sessions",
            "B) It allows the LLM to reason about what it knows, what it needs, and which tool to call next — making the decision process transparent and debuggable",
            "C) It validates the syntax of the function call before sending it to the tool",
            "D) It compresses the conversation history to save context window tokens",
        ],
        "correct_answer": (
            "B) It allows the LLM to reason about what it knows, what it needs, and which tool "
            "to call next — making the decision process transparent and debuggable"
        ),
        "explanation": (
            "ReAct interleaves Thought (internal reasoning), Action (tool call), and "
            "Observation (tool result) in a loop. The Thought step is a scratchpad where "
            "the model explicitly reasons before committing to an action. This improves "
            "reliability (the model 'thinks before acting'), enables better error recovery, "
            "and makes the agent's decision-making fully auditable — a critical property "
            "for production AI systems."
        ),
        "remember": "ReAct loop: Thought → Action → Observation → repeat. Thought = reasoning scratchpad. Makes agents debuggable.",
    },
    {
        "type": "coding",
        "difficulty": "hard",
        "topic": "DSA — Tree / recursion",
        "question": (
            "Given the root of a binary tree, return the maximum depth (number of nodes "
            "along the longest root-to-leaf path).\n\n"
            "Examples:\n"
            "  Tree: [3,9,20,null,null,15,7]\n"
            "       3\n"
            "      / \\\n"
            "     9  20\n"
            "       /  \\\n"
            "      15   7\n"
            "  max_depth(root)  →  3\n\n"
            "  Tree: [1,null,2]  →  2\n\n"
            "Solve recursively. Bonus: also show the iterative BFS approach."
        ),
        "language": "python",
        "starter_code": (
            "class TreeNode:\n"
            "    def __init__(self, val=0, left=None, right=None):\n"
            "        self.val = val\n"
            "        self.left = left\n"
            "        self.right = right\n"
            "\n\n"
            "def max_depth(root: TreeNode) -> int:\n"
            '    """\n'
            "    Return the maximum depth of the binary tree.\n"
            "    Time: O(n), Space: O(h) where h = height\n"
            '    """\n'
            "    pass\n"
        ),
        "correct_answer": (
            "# Recursive (DFS)\n"
            "def max_depth(root):\n"
            "    if root is None:\n"
            "        return 0\n"
            "    return 1 + max(max_depth(root.left), max_depth(root.right))\n"
            "\n"
            "# Iterative (BFS — level order)\n"
            "from collections import deque\n"
            "def max_depth_bfs(root):\n"
            "    if not root:\n"
            "        return 0\n"
            "    depth, queue = 0, deque([root])\n"
            "    while queue:\n"
            "        depth += 1\n"
            "        for _ in range(len(queue)):\n"
            "            node = queue.popleft()\n"
            "            if node.left:  queue.append(node.left)\n"
            "            if node.right: queue.append(node.right)\n"
            "    return depth\n"
        ),
        "explanation": (
            "The recursive approach is the cleanest: depth of a node = 1 + max depth of "
            "its subtrees. Base case: None → 0. Time O(n) — every node visited once. "
            "Space O(h) for the call stack (O(log n) balanced, O(n) worst case skewed). "
            "BFS counts levels: process the queue level by level, incrementing depth each "
            "time. Both are O(n) time. Know both — interviewers often ask for the 'other' one."
        ),
        "remember": "Tree depth: recursion = 1 + max(left, right). BFS level order = count levels. Know both patterns.",
    },
]
