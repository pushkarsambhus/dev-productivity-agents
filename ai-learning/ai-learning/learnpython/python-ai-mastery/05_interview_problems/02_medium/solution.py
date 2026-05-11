"""
SOLUTION: Phase 5 | Interview Problems | 02 Medium
"""
from collections import defaultdict, Counter
import heapq


# ── 1. LRU Cache Manual ────────────────────────────────────────────────────────
class DLinkedNode:
    def __init__(self, key="", val=None):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None


class LRUCacheManual:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache: dict[str, DLinkedNode] = {}
        self.head = DLinkedNode()   # LRU sentinel
        self.tail = DLinkedNode()   # MRU sentinel
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: DLinkedNode):
        node.prev.next = node.next
        node.next.prev = node.prev
        # Unlinking: bypass node on both sides

    def _add_to_tail(self, node: DLinkedNode):
        node.prev = self.tail.prev
        node.next = self.tail
        self.tail.prev.next = node
        self.tail.prev = node
        # Insert before sentinel tail = mark as most recently used

    def get(self, key: str) -> any:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._remove(node)
        self._add_to_tail(node)
        return node.val

    def put(self, key: str, val: any):
        if key in self.cache:
            node = self.cache[key]
            node.val = val
            self._remove(node)
            self._add_to_tail(node)
        else:
            node = DLinkedNode(key, val)
            self.cache[key] = node
            self._add_to_tail(node)
            if len(self.cache) > self.capacity:
                lru = self.head.next   # node after LRU sentinel = least recently used
                self._remove(lru)
                del self.cache[lru.key]


# ── 2. Minimum Window Substring ───────────────────────────────────────────────
def min_window(s: str, t: str) -> str:
    if not t or not s:
        return ""
    need = Counter(t)
    have = defaultdict(int)
    formed = 0             # how many chars in `t` are satisfied
    required = len(need)   # how many distinct chars need to be satisfied
    left = 0
    best = (float("inf"), 0, 0)   # (length, left, right)

    for right, ch in enumerate(s):
        have[ch] += 1
        if ch in need and have[ch] == need[ch]:
            formed += 1
        # Shrink window from left while all chars are satisfied
        while formed == required:
            if (right - left + 1) < best[0]:
                best = (right - left + 1, left, right)
            have[s[left]] -= 1
            if s[left] in need and have[s[left]] < need[s[left]]:
                formed -= 1
            left += 1

    return "" if best[0] == float("inf") else s[best[1]:best[2]+1]
    # Classic sliding window: expand right freely, shrink left when constraint met.
    # `formed` tracks when we've satisfied ALL character requirements.


# ── 3. Number of Islands ──────────────────────────────────────────────────────
def num_islands(grid: list[list[str]]) -> int:
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])
    count = 0

    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != "1":
            return
        grid[r][c] = "0"   # mark visited by sinking the island
        dfs(r+1, c); dfs(r-1, c); dfs(r, c+1); dfs(r, c-1)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                dfs(r, c)   # sink the entire island
                count += 1
    return count
    # Mutating the grid avoids a separate visited set.
    # If you can't mutate: use a set() of (r, c) tuples.


# ── 4. Top K Frequent ─────────────────────────────────────────────────────────
def top_k_frequent(nums: list[int], k: int) -> list[int]:
    counts = Counter(nums)
    # heapq.nlargest: O(n log k) — better than full sort O(n log n) for small k
    return [item for item, _ in heapq.nlargest(k, counts.items(), key=lambda x: x[1])]


# ── 5. Merge Intervals ────────────────────────────────────────────────────────
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    intervals.sort(key=lambda x: x[0])   # sort by start time
    merged = [intervals[0]]
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:        # overlaps with last interval
            merged[-1][1] = max(merged[-1][1], end)   # extend end
        else:
            merged.append([start, end])
    return merged
    # Key: after sorting, only need to check against the LAST merged interval.


if __name__ == "__main__":
    print("=== LRU Manual ===")
    lru = LRUCacheManual(2)
    lru.put("a", 1); lru.put("b", 2)
    print(lru.get("a"))
    lru.put("c", 3)
    print(lru.get("b"))
    print(lru.get("c"))

    print("\n=== Min Window ===")
    print(min_window("ADOBECODEBANC", "ABC"))
    print(min_window("a", "a"))
    print(min_window("a", "aa"))

    print("\n=== Num Islands ===")
    grid1 = [["1","1","0","0","0"],["1","1","0","0","0"],
             ["0","0","1","0","0"],["0","0","0","1","1"]]
    print(num_islands(grid1))

    print("\n=== Top K ===")
    print(top_k_frequent([1,1,1,2,2,3], 2))
    print(top_k_frequent([1], 1))

    print("\n=== Merge Intervals ===")
    print(merge_intervals([[1,3],[2,6],[8,10],[15,18]]))
    print(merge_intervals([[1,4],[4,5]]))
