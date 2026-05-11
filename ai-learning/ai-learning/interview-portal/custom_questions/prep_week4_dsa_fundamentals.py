"""
Coding Interview Prep — Week 4-5: DSA Fundamentals & Patterns
=============================================================
Covers: Big O, Two Pointers, Sliding Window, Hash Maps/Sets,
        Stacks & Queues, Recursion, Dynamic Programming, Binary Search
"""

NAME        = "Week 4-5: DSA Fundamentals"
DESCRIPTION = "Two pointers, sliding window, hash maps, stacks, recursion, DP, binary search"
ICON        = "🧩"

CONCEPTS = [
    {
        "title": "Big O & Complexity Analysis",
        "explanation": """Big O describes how runtime or memory **scales** as input grows. Ignore constants, keep the dominant term.

| Big O | Name | Example |
|-------|------|---------|
| O(1) | Constant | dict lookup, array index |
| O(log n) | Logarithmic | binary search |
| O(n) | Linear | single loop |
| O(n log n) | Linearithmic | sort |
| O(n²) | Quadratic | nested loops |
| O(2ⁿ) | Exponential | naive recursion (Fibonacci) |

**Rules:**
- Drop constants: O(2n) → O(n)
- Drop lower terms: O(n² + n) → O(n²)
- Always state both **time** AND **space** complexity

**Common patterns:**
```python
# O(n) — one pass
for x in nums: ...

# O(n²) — nested loops
for i in nums:
    for j in nums: ...

# O(log n) — halving search space
left, right = 0, len(nums) - 1
while left <= right:
    mid = (left + right) // 2
    ...
```""",
        "gotchas": [
            "dict/set lookup is O(1) average — this is why you use them to replace O(n) list scans.",
            "Python list.pop(0) is O(n) — use collections.deque.popleft() which is O(1).",
            "Sorting is always O(n log n) — never assume a faster sort exists for general data.",
        ],
        "videos": [
            {"title": "Big O Notation (freeCodeCamp)", "url": "https://www.youtube.com/watch?v=Mo4vesaut8g", "source": "YouTube"},
            {"title": "Big O for Coding Interviews (NeetCode)", "url": "https://www.youtube.com/watch?v=BgLTDT03QtU", "source": "YouTube"},
            {"title": "Master the Coding Interview: Data Structures & Algorithms", "url": "https://www.udemy.com/course/master-the-coding-interview-data-structures-algorithms/", "source": "Udemy"},
        ],
    },
    {
        "title": "Two Pointers Pattern",
        "explanation": """Use two pointers moving toward (or away from) each other to avoid nested loops.

**Trigger:** sorted array + find pair/triplet with target sum, or compare from both ends.

**Template:**
```python
left, right = 0, len(nums) - 1
while left < right:
    current = nums[left] + nums[right]
    if current == target:
        return True
    elif current < target:
        left += 1    # need bigger sum
    else:
        right -= 1   # need smaller sum
return False
```

**Why it works:** Array is sorted — moving left right increases the sum, moving right left decreases it. Covers all possibilities in O(n) instead of O(n²).

**Other two-pointer uses:**
- Remove duplicates from sorted array
- Reverse a string/array in-place
- Check palindrome""",
        "gotchas": [
            "Only works on SORTED arrays for sum problems.",
            "Condition is left < right (not <=) to avoid using the same element twice.",
            "For non-sorted: use a hash set instead (O(n) space trade-off).",
        ],
        "videos": [
            {"title": "Two Pointers Pattern (NeetCode)", "url": "https://www.youtube.com/watch?v=On03HWe2tZM", "source": "YouTube"},
            {"title": "Two Sum — LeetCode #1 (NeetCode)", "url": "https://www.youtube.com/watch?v=KLlXCFG5TnA", "source": "YouTube"},
            {"title": "Master the Coding Interview — Arrays section", "url": "https://www.udemy.com/course/master-the-coding-interview-data-structures-algorithms/", "source": "Udemy"},
        ],
    },
    {
        "title": "Sliding Window Pattern",
        "explanation": """Use a window that slides across the array to avoid recomputing overlapping subarray sums/counts.

**Trigger:** contiguous subarray/substring + max/min/count + fixed or variable size window.

**Fixed-size window template:**
```python
# Max sum of subarray of size k
window_sum = sum(nums[:k])
max_sum = window_sum
for i in range(k, len(nums)):
    window_sum += nums[i] - nums[i - k]   # slide: add new, remove old
    max_sum = max(max_sum, window_sum)
```

**Variable-size window template:**
```python
# Longest substring with at most k distinct chars
left = 0
counts = {}
for right in range(len(s)):
    counts[s[right]] = counts.get(s[right], 0) + 1
    while len(counts) > k:          # shrink window from left
        counts[s[left]] -= 1
        if counts[s[left]] == 0:
            del counts[s[left]]
        left += 1
    max_len = max(max_len, right - left + 1)
```""",
        "gotchas": [
            "Fixed window: always add the new right element AND remove the old left element.",
            "Variable window: expand right, shrink left when constraint violated.",
            "Window size formula: right - left + 1.",
        ],
        "videos": [
            {"title": "Sliding Window Pattern (NeetCode)", "url": "https://www.youtube.com/watch?v=p-ss2JNynmw", "source": "YouTube"},
            {"title": "Sliding Window Technique (Abdul Bari)", "url": "https://www.youtube.com/watch?v=MK-NZ4hN7rs", "source": "YouTube"},
            {"title": "Master the Coding Interview — Strings section", "url": "https://www.udemy.com/course/master-the-coding-interview-data-structures-algorithms/", "source": "Udemy"},
        ],
    },
    {
        "title": "Hash Maps & Sets",
        "explanation": """**Hash map** = dict. **Hash set** = set. Both give O(1) average lookup.

**Interview pattern — frequency count:**
```python
from collections import Counter
counts = Counter("hello")   # {"h":1, "e":1, "l":2, "o":1}

# Manual version:
counts = {}
for c in s:
    counts[c] = counts.get(c, 0) + 1
```

**Interview pattern — fast lookup (replace O(n) search):**
```python
# Find two numbers that sum to target
seen = set()
for n in nums:
    if target - n in seen:   # O(1) lookup instead of O(n) scan
        return True
    seen.add(n)
```

**Grouping pattern:**
```python
from collections import defaultdict
groups = defaultdict(list)
for word in words:
    key = "".join(sorted(word))   # anagram key
    groups[key].append(word)
```""",
        "gotchas": [
            "dict/set lookup is O(1) average, O(n) worst case (hash collision — rare).",
            "Keys must be hashable: str, int, tuple are OK. list, dict are NOT.",
            "Counter is a subclass of dict — all dict methods work on it.",
        ],
        "videos": [
            {"title": "Hash Tables (NeetCode)", "url": "https://www.youtube.com/watch?v=KyUTuwz_b7Q", "source": "YouTube"},
            {"title": "Python defaultdict & Counter (Tech With Tim)", "url": "https://www.youtube.com/watch?v=7abBWAEiGX4", "source": "YouTube"},
            {"title": "Master the Coding Interview — Hash Tables section", "url": "https://www.udemy.com/course/master-the-coding-interview-data-structures-algorithms/", "source": "Udemy"},
        ],
    },
    {
        "title": "Stacks & Queues",
        "explanation": """**Stack** — LIFO (Last In First Out). Like Java's Stack or Deque.
```python
stack = []
stack.append(x)   # push   → Java: stack.push(x)
stack.pop()       # pop    → Java: stack.pop()
stack[-1]         # peek   → Java: stack.peek()
```

**Queue** — FIFO (First In First Out). Use collections.deque (NOT list).
```python
from collections import deque
q = deque()
q.append(x)       # enqueue → add to right
q.popleft()       # dequeue → remove from left — O(1)
# list.pop(0) is O(n) — never use it as a queue!
```

**Stack trigger words:** matching brackets, undo/redo, call stack simulation, "most recent".
**Queue trigger words:** BFS, level-order traversal, "process in order".

**Monotonic stack** (advanced):
```python
# Next greater element pattern
stack = []
for i, n in enumerate(nums):
    while stack and n > nums[stack[-1]]:
        idx = stack.pop()
        result[idx] = n
    stack.append(i)
```""",
        "gotchas": [
            "Use deque for queues — list.pop(0) is O(n). deque.popleft() is O(1).",
            "Stack peek = stack[-1], not stack.peek().",
            "Empty stack check: if not stack: (not if stack == []:)",
        ],
        "videos": [
            {"title": "Stack Data Structure (NeetCode)", "url": "https://www.youtube.com/watch?v=O1KeXo8lE8A", "source": "YouTube"},
            {"title": "Queue in Python (Tech With Tim)", "url": "https://www.youtube.com/watch?v=rUUrmGKYwHw", "source": "YouTube"},
            {"title": "Master the Coding Interview — Stacks & Queues", "url": "https://www.udemy.com/course/master-the-coding-interview-data-structures-algorithms/", "source": "Udemy"},
        ],
    },
    {
        "title": "Recursion & Dynamic Programming",
        "explanation": """**Recursion:** function calls itself with a smaller input until base case.
```python
def fib(n):
    if n <= 1: return n           # base case
    return fib(n-1) + fib(n-2)   # recursive case
```
Every recursion needs: **base case + recursive case + progress toward base case**.

**Memoization** (top-down DP) — cache results:
```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    if n <= 1: return n
    return fib(n-1) + fib(n-2)
# O(2^n) → O(n) with caching
```

**Bottom-up DP** — build solution from smallest subproblems:
```python
# Fibonacci iteratively
dp = [0, 1]
for i in range(2, n+1):
    dp.append(dp[i-1] + dp[i-2])
return dp[n]
```

**DP trigger:** overlapping subproblems + optimal substructure = "can I reuse previous answers?"

**Binary Search:**
```python
left, right = 0, len(nums) - 1
while left <= right:
    mid = left + (right - left) // 2   # avoids overflow
    if nums[mid] == target: return mid
    elif nums[mid] < target: left = mid + 1
    else: right = mid - 1
return -1
```""",
        "gotchas": [
            "Recursion without base case = infinite loop / stack overflow.",
            "mid = left + (right-left)//2 not (left+right)//2 — avoids integer overflow (Java habit).",
            "Binary search condition: left <= right (with equals).",
            "DP = recursion + memoization. If you can define dp[i] in terms of smaller dp values, use DP.",
        ],
        "videos": [
            {"title": "Recursion (freeCodeCamp)", "url": "https://www.youtube.com/watch?v=IJDJ0kBx2LM", "source": "YouTube"},
            {"title": "Dynamic Programming (NeetCode — full playlist)", "url": "https://www.youtube.com/watch?v=73r3KWiEvyk", "source": "YouTube"},
            {"title": "Binary Search (NeetCode)", "url": "https://www.youtube.com/watch?v=s4DPM8ct1pI", "source": "YouTube"},
            {"title": "Master the Coding Interview — Recursion & DP", "url": "https://www.udemy.com/course/master-the-coding-interview-data-structures-algorithms/", "source": "Udemy"},
        ],
    },
]

QUESTIONS = [

    # ══════════════════════════════════════════════════════════════════
    # BIG O
    # ══════════════════════════════════════════════════════════════════
    {
        "type": "mcq",
        "difficulty": "easy",
        "topic": "Big O Notation",
        "question": (
            "What is the time complexity of looking up a key in a Python dict?"
        ),
        "options": [
            "A) O(n)",
            "B) O(log n)",
            "C) O(1) average",
            "D) O(n log n)",
        ],
        "correct_answer": "C) O(1) average",
        "explanation": (
            "Python dicts are hash tables. On average, key lookup is O(1) because the hash function "
            "maps the key directly to a bucket. Worst case is O(n) due to hash collisions, "
            "but this is rare in practice. Same applies to set membership ('x in my_set'). "
            "This is why dicts and sets are the go-to data structure for fast lookups in interviews. "
            "Java's HashMap has the same O(1) average complexity."
        ),
        "remember": "dict/set lookup = O(1) average. This is why you use them to replace O(n) list searches.",
    },
    {
        "type": "mcq",
        "difficulty": "medium",
        "topic": "Big O Notation",
        "question": (
            "What is the time and space complexity of this function?\n\n"
            "    def find_duplicates(nums):\n"
            "        seen = set()\n"
            "        dups = []\n"
            "        for n in nums:\n"
            "            if n in seen:\n"
            "                dups.append(n)\n"
            "            seen.add(n)\n"
            "        return dups"
        ),
        "options": [
            "A) O(n²) time, O(1) space",
            "B) O(n) time, O(n) space",
            "C) O(n log n) time, O(n) space",
            "D) O(n) time, O(1) space",
        ],
        "correct_answer": "B) O(n) time, O(n) space",
        "explanation": (
            "The loop runs once over n elements — O(n). Each 'n in seen' and 'seen.add(n)' is O(1) average. "
            "The set 'seen' can grow to hold all n elements in the worst case — O(n) space. "
            "This is the classic trade-off: use O(n) extra space to achieve O(n) time instead of O(n²). "
            "The naive approach (nested loops) would be O(n²) time, O(1) space."
        ),
        "remember": "Set/dict for fast lookup = O(n) space trade-off. Always state both time AND space complexity.",
    },

    # ══════════════════════════════════════════════════════════════════
    # TWO POINTERS
    # ══════════════════════════════════════════════════════════════════
    {
        "type": "coding",
        "difficulty": "easy",
        "topic": "Two Pointers",
        "question": (
            "Given a SORTED array and a target, return True if any two numbers sum to target.\n\n"
            "Use two pointers — do NOT use a hash set.\n\n"
            "Examples:\n"
            "  two_sum_sorted([1,2,3,4,6], 6) → True  (2+4)\n"
            "  two_sum_sorted([1,2,3,4,6], 10) → False\n"
            "  two_sum_sorted([1,5], 6) → True"
        ),
        "language": "python",
        "starter_code": (
            "def two_sum_sorted(nums: list, target: int) -> bool:\n"
            "    pass\n"
        ),
        "correct_answer": (
            "def two_sum_sorted(nums: list, target: int) -> bool:\n"
            "    left, right = 0, len(nums) - 1\n"
            "    while left < right:\n"
            "        s = nums[left] + nums[right]\n"
            "        if s == target:\n"
            "            return True\n"
            "        elif s < target:\n"
            "            left += 1\n"
            "        else:\n"
            "            right -= 1\n"
            "    return False\n"
        ),
        "explanation": (
            "Two pointers work on sorted arrays. Start left=0, right=end. "
            "If sum < target, move left pointer right (increase sum). "
            "If sum > target, move right pointer left (decrease sum). "
            "O(n) time, O(1) space — much better than hash set O(n) space or nested loops O(n²). "
            "Trigger words: sorted array + pair/triplet sum → Two Pointers."
        ),
        "remember": "Two Pointers trigger: sorted array + find pair. Move left up if sum too small, right down if too big.",
    },

    # ══════════════════════════════════════════════════════════════════
    # SLIDING WINDOW
    # ══════════════════════════════════════════════════════════════════
    {
        "type": "coding",
        "difficulty": "medium",
        "topic": "Sliding Window",
        "question": (
            "Given an array of integers and k, return the maximum sum of any contiguous subarray of size k.\n\n"
            "Examples:\n"
            "  max_subarray_sum([2,1,5,1,3,2], 3) → 9  (5+1+3)\n"
            "  max_subarray_sum([2,3,4,1,5], 2)   → 7  (3+4)\n"
            "  max_subarray_sum([1,2,3], 1)         → 3"
        ),
        "language": "python",
        "starter_code": (
            "def max_subarray_sum(nums: list, k: int) -> int:\n"
            "    pass\n"
        ),
        "correct_answer": (
            "def max_subarray_sum(nums: list, k: int) -> int:\n"
            "    window_sum = sum(nums[:k])\n"
            "    max_sum = window_sum\n"
            "    for i in range(k, len(nums)):\n"
            "        window_sum += nums[i] - nums[i - k]\n"
            "        max_sum = max(max_sum, window_sum)\n"
            "    return max_sum\n"
        ),
        "explanation": (
            "Sliding window avoids recomputing the sum from scratch each time. "
            "Compute the first window, then slide: add the new right element, subtract the old left element. "
            "O(n) time, O(1) space — vs the naive O(n*k) nested loop approach. "
            "Trigger words: contiguous subarray/substring + fixed or variable size → Sliding Window."
        ),
        "remember": "Sliding Window: add new right element, remove old left element. Avoids recomputing the whole window each step.",
    },

    # ══════════════════════════════════════════════════════════════════
    # HASH MAPS
    # ══════════════════════════════════════════════════════════════════
    {
        "type": "coding",
        "difficulty": "medium",
        "topic": "Hash Maps",
        "question": (
            "Given two strings, return True if they are anagrams of each other.\n\n"
            "Examples:\n"
            "  is_anagram('anagram', 'nagaram') → True\n"
            "  is_anagram('rat', 'car')          → False\n"
            "  is_anagram('listen', 'silent')    → True"
        ),
        "language": "python",
        "starter_code": (
            "def is_anagram(s: str, t: str) -> bool:\n"
            "    pass\n"
        ),
        "correct_answer": (
            "def is_anagram(s: str, t: str) -> bool:\n"
            "    if len(s) != len(t):\n"
            "        return False\n"
            "    count = {}\n"
            "    for c in s:\n"
            "        count[c] = count.get(c, 0) + 1\n"
            "    for c in t:\n"
            "        count[c] = count.get(c, 0) - 1\n"
            "    return all(v == 0 for v in count.values())\n"
            "\n"
            "# Cleaner alternative:\n"
            "# from collections import Counter\n"
            "# return Counter(s) == Counter(t)\n"
        ),
        "explanation": (
            "Anagram check = same characters, same frequencies. "
            "Count characters in s, decrement for t, all counts should be 0. "
            "O(n) time, O(1) space (at most 26 lowercase letters in the map). "
            "sorted(s) == sorted(t) also works but is O(n log n). "
            "Trigger words: anagram, permutation, same characters → frequency map."
        ),
        "remember": "Anagram = frequency map equality. Counter(s) == Counter(t) is the clean one-liner.",
    },

    # ══════════════════════════════════════════════════════════════════
    # STACKS & QUEUES
    # ══════════════════════════════════════════════════════════════════
    {
        "type": "coding",
        "difficulty": "medium",
        "topic": "Stacks",
        "question": (
            "Given a string of brackets, return True if it is valid (all brackets are properly closed).\n\n"
            "Examples:\n"
            "  is_valid('()[]{}')  → True\n"
            "  is_valid('([)]')    → False\n"
            "  is_valid('{[]}')    → True\n"
            "  is_valid('(')       → False"
        ),
        "language": "python",
        "starter_code": (
            "def is_valid(s: str) -> bool:\n"
            "    pass\n"
        ),
        "correct_answer": (
            "def is_valid(s: str) -> bool:\n"
            "    stack = []\n"
            "    pairs = {')': '(', ']': '[', '}': '{'}\n"
            "    for c in s:\n"
            "        if c in '([{':\n"
            "            stack.append(c)\n"
            "        elif c in ')]}':\n"
            "            if not stack or stack[-1] != pairs[c]:\n"
            "                return False\n"
            "            stack.pop()\n"
            "    return len(stack) == 0\n"
        ),
        "explanation": (
            "Stack (LIFO) is the natural data structure for matching brackets. "
            "Push opening brackets. For closing brackets, check that the top of the stack "
            "is the matching opener. If not, or stack is empty, return False. "
            "After processing, stack must be empty (all brackets closed). "
            "Python list is used as a stack: append() = push, pop() = pop, [-1] = peek. "
            "Trigger words: matching/balanced pairs, undo/redo, call stack simulation → Stack."
        ),
        "remember": "Stack trigger: matching pairs, nested structures. Python list as stack: append/pop/[-1].",
    },

    # ══════════════════════════════════════════════════════════════════
    # RECURSION + FIBONACCI
    # ══════════════════════════════════════════════════════════════════
    {
        "type": "coding",
        "difficulty": "easy",
        "topic": "Recursion",
        "question": (
            "Implement Fibonacci using recursion with memoization.\n\n"
            "fib(0) = 0, fib(1) = 1, fib(n) = fib(n-1) + fib(n-2)\n\n"
            "Examples:\n"
            "  fib(0)  → 0\n"
            "  fib(5)  → 5\n"
            "  fib(10) → 55"
        ),
        "language": "python",
        "starter_code": (
            "def fib(n: int, memo: dict = None) -> int:\n"
            "    pass\n"
        ),
        "correct_answer": (
            "def fib(n: int, memo: dict = None) -> int:\n"
            "    if memo is None:\n"
            "        memo = {}\n"
            "    if n <= 1:\n"
            "        return n\n"
            "    if n in memo:\n"
            "        return memo[n]\n"
            "    memo[n] = fib(n - 1, memo) + fib(n - 2, memo)\n"
            "    return memo[n]\n"
            "\n"
            "# Alternative with functools.lru_cache:\n"
            "# from functools import lru_cache\n"
            "# @lru_cache(maxsize=None)\n"
            "# def fib(n): return n if n <= 1 else fib(n-1) + fib(n-2)\n"
        ),
        "explanation": (
            "Naive recursion is O(2^n) — it recomputes the same values. "
            "Memoization caches results, reducing to O(n) time and O(n) space. "
            "Every recursion needs: base case + recursive case + progress toward base case. "
            "Note: memo=None default avoids the mutable default argument trap. "
            "lru_cache is the production-clean version. Know both for interviews."
        ),
        "remember": "Recursion = base case + recursive case. Always add memoization for overlapping subproblems (O(2^n) → O(n)).",
    },

    # ══════════════════════════════════════════════════════════════════
    # BINARY SEARCH
    # ══════════════════════════════════════════════════════════════════
    {
        "type": "coding",
        "difficulty": "medium",
        "topic": "Binary Search",
        "question": (
            "Implement binary search. Return the index of target in a sorted array, or -1 if not found.\n\n"
            "Examples:\n"
            "  binary_search([1,3,5,7,9], 5)  → 2\n"
            "  binary_search([1,3,5,7,9], 6)  → -1\n"
            "  binary_search([1], 1)            → 0"
        ),
        "language": "python",
        "starter_code": (
            "def binary_search(nums: list, target: int) -> int:\n"
            "    pass\n"
        ),
        "correct_answer": (
            "def binary_search(nums: list, target: int) -> int:\n"
            "    left, right = 0, len(nums) - 1\n"
            "    while left <= right:\n"
            "        mid = left + (right - left) // 2\n"
            "        if nums[mid] == target:\n"
            "            return mid\n"
            "        elif nums[mid] < target:\n"
            "            left = mid + 1\n"
            "        else:\n"
            "            right = mid - 1\n"
            "    return -1\n"
        ),
        "explanation": (
            "Binary search halves the search space each iteration — O(log n). "
            "Use mid = left + (right - left) // 2, NOT (left + right) // 2, to avoid integer overflow "
            "(critical in Java/C++, less so in Python but good habit). "
            "The condition is left <= right (not <). "
            "After the loop, if target not found, return -1. "
            "Trigger words: sorted array + search/find → Binary Search."
        ),
        "remember": "Binary search: O(log n). Condition left <= right. mid = left + (right-left)//2 avoids overflow.",
    },

    # ══════════════════════════════════════════════════════════════════
    # DYNAMIC PROGRAMMING
    # ══════════════════════════════════════════════════════════════════
    {
        "type": "coding",
        "difficulty": "hard",
        "topic": "Dynamic Programming",
        "question": (
            "Given an array of non-negative integers representing coin denominations and a target amount, "
            "return the minimum number of coins needed to make up that amount. "
            "Return -1 if it's not possible.\n\n"
            "Examples:\n"
            "  coin_change([1,5,6,9], 11) → 2  (5+6)\n"
            "  coin_change([1,2,5], 11)   → 3  (5+5+1)\n"
            "  coin_change([2], 3)         → -1"
        ),
        "language": "python",
        "starter_code": (
            "def coin_change(coins: list, amount: int) -> int:\n"
            "    pass\n"
        ),
        "correct_answer": (
            "def coin_change(coins: list, amount: int) -> int:\n"
            "    dp = [float('inf')] * (amount + 1)\n"
            "    dp[0] = 0\n"
            "    for i in range(1, amount + 1):\n"
            "        for coin in coins:\n"
            "            if coin <= i:\n"
            "                dp[i] = min(dp[i], dp[i - coin] + 1)\n"
            "    return dp[amount] if dp[amount] != float('inf') else -1\n"
        ),
        "explanation": (
            "Bottom-up DP. dp[i] = min coins to make amount i. "
            "Base case: dp[0] = 0 (0 coins to make amount 0). "
            "Transition: dp[i] = min(dp[i], dp[i - coin] + 1) for each coin <= i. "
            "Initialize with infinity to represent 'not reachable'. "
            "If dp[amount] is still infinity, return -1. "
            "Time: O(amount * len(coins)), Space: O(amount). "
            "Trigger words: min/max ways to reach amount, count combinations → DP."
        ),
        "remember": "DP trigger: optimal substructure + overlapping subproblems. Coin change = classic unbounded knapsack variant.",
    },
]
