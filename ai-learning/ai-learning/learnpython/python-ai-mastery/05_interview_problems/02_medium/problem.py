"""
PHASE 5 | INTERVIEW PROBLEMS | 02 MEDIUM
=========================================
These are the core interview tier — expect 1-2 of these in any principal-level
coding screen. Target: solve each in 15-20 minutes with clean code.
"""
from collections import defaultdict, deque


# ── 1. LRU Cache (implement from scratch) ────────────────────────────────────
# You saw this in Phase 3. Now implement it WITHOUT OrderedDict — use a
# doubly linked list + hashmap. This is the LeetCode #146 hard variant.
# Interviewers ask this to test data structure composition.

class DLinkedNode:
    def __init__(self, key="", val=None):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None


class LRUCacheManual:
    """O(1) get and put using doubly linked list + hashmap."""

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache: dict[str, DLinkedNode] = {}
        # Sentinel nodes: head (LRU side) ↔ ... ↔ tail (MRU side)
        self.head = DLinkedNode()
        self.tail = DLinkedNode()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: DLinkedNode):
        """Unlink node from list."""
        # TODO: update prev and next pointers
        pass

    def _add_to_tail(self, node: DLinkedNode):
        """Insert node just before tail (most recently used position)."""
        # TODO
        pass

    def get(self, key: str) -> any:
        # TODO: if found, move to tail, return val. else -1.
        pass

    def put(self, key: str, val: any):
        # TODO: if exists, update + move to tail.
        # If new: add to tail, evict head.next if over capacity.
        pass


# ── 2. Minimum Window Substring ──────────────────────────────────────────────
# Given strings s and t, find the minimum window in s that contains all
# characters of t. Return "" if no such window.
# Example: s="ADOBECODEBANC", t="ABC" → "BANC"
# Pattern: sliding window + two frequency counters

def min_window(s: str, t: str) -> str:
    pass


# ── 3. Number of Islands ─────────────────────────────────────────────────────
# Given a 2D grid of '1' (land) and '0' (water), count the islands.
# An island is surrounded by water and formed by connecting adjacent land.
# Use DFS — mark visited cells to avoid re-counting.

def num_islands(grid: list[list[str]]) -> int:
    pass


# ── 4. Top K Frequent Elements ───────────────────────────────────────────────
# Given a list and integer k, return the k most frequent elements.
# Example: [1,1,1,2,2,3], k=2 → [1,2]
# Optimal: bucket sort approach O(n), or heap approach O(n log k).
# Implement the heap approach using heapq.

import heapq

def top_k_frequent(nums: list[int], k: int) -> list[int]:
    pass


# ── 5. Merge Intervals ────────────────────────────────────────────────────────
# Given a list of intervals [start, end], merge all overlapping intervals.
# [[1,3],[2,6],[8,10],[15,18]] → [[1,6],[8,10],[15,18]]
# Use case: merging time windows in scheduler, token overlap in chunking.

def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    pass


# ── Self-check ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== LRU Manual ===")
    lru = LRUCacheManual(2)
    lru.put("a", 1)
    lru.put("b", 2)
    print(lru.get("a"))    # 1
    lru.put("c", 3)        # evicts "b"
    print(lru.get("b"))    # -1
    print(lru.get("c"))    # 3

    print("\n=== Min Window ===")
    print(min_window("ADOBECODEBANC", "ABC"))   # "BANC"
    print(min_window("a", "a"))                  # "a"
    print(min_window("a", "aa"))                 # ""

    print("\n=== Num Islands ===")
    grid1 = [["1","1","0","0","0"],
             ["1","1","0","0","0"],
             ["0","0","1","0","0"],
             ["0","0","0","1","1"]]
    print(num_islands(grid1))   # 3

    print("\n=== Top K ===")
    print(top_k_frequent([1,1,1,2,2,3], 2))   # [1, 2]
    print(top_k_frequent([1], 1))               # [1]

    print("\n=== Merge Intervals ===")
    print(merge_intervals([[1,3],[2,6],[8,10],[15,18]]))   # [[1,6],[8,10],[15,18]]
    print(merge_intervals([[1,4],[4,5]]))                   # [[1,5]]
