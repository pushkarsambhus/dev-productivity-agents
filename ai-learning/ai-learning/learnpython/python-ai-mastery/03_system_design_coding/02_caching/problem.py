"""
PHASE 3 | SYSTEM DESIGN CODING | 02 CACHING
============================================
Topic: LRU Cache — one of the most commonly asked system design coding problems.
Appears in: LLM semantic caches, embedding caches, API response caches.

LRU = Least Recently Used. When cache is full, evict the item used longest ago.

Optimal implementation: O(1) get AND put → OrderedDict or dict + doubly linked list.
For interviews: use Python's OrderedDict — it's the intended idiomatic solution.
"""
from collections import OrderedDict


class LRUCache:
    """
    LRU Cache with O(1) get and put.

    Args:
        capacity: maximum number of items to store
    """

    def __init__(self, capacity: int):
        # TODO: store capacity, initialize an OrderedDict
        # OrderedDict remembers insertion order AND supports move_to_end()
        pass

    def get(self, key: str) -> any:
        """
        Return value for key, or -1 if not found.
        Accessing a key marks it as most recently used.
        """
        # TODO:
        # If key exists: move it to end (most recent), return value
        # If key missing: return -1
        pass

    def put(self, key: str, value: any):
        """
        Insert or update key-value pair.
        If key exists, update and mark as most recently used.
        If at capacity, evict least recently used (front of OrderedDict).
        """
        # TODO:
        # If key exists: move to end, update value
        # Else: add to end
        # If over capacity: pop from front (least recently used)
        pass

    def __repr__(self):
        return f"LRUCache({dict(self.cache)})"


# ── Bonus: Embedding Cache ─────────────────────────────────────────────────────
# A practical wrapper that caches embedding API calls by text content.

class EmbeddingCache:
    """
    Wraps an embedding function with LRU caching.
    Avoids re-calling the (expensive) embedding API for repeated text.
    """

    def __init__(self, embed_fn: callable, capacity: int = 500):
        # TODO: store embed_fn, create an LRUCache
        pass

    def embed(self, text: str) -> list[float]:
        """Return embedding, using cache if available."""
        # TODO: check cache first, call embed_fn on miss, store result
        pass

    @property
    def cache_size(self) -> int:
        pass


# ── Self-check ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== LRU Cache ===")
    cache = LRUCache(capacity=3)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("c", 3)
    print(cache.get("a"))    # 1 — also marks "a" as most recently used
    cache.put("d", 4)        # evicts "b" (least recently used after "a" was accessed)
    print(cache.get("b"))    # -1 — evicted
    print(cache.get("c"))    # 3
    print(cache.get("d"))    # 4
    print(cache)

    print("\n=== Embedding Cache ===")
    call_count = 0

    def fake_embed(text: str) -> list[float]:
        global call_count
        call_count += 1
        return [len(text) * 0.01, 0.5]  # fake embedding

    ec = EmbeddingCache(fake_embed, capacity=10)
    ec.embed("hello world")
    ec.embed("hello world")   # should be cached — no API call
    ec.embed("different text")
    print(f"API calls made: {call_count}")   # should be 2, not 3
    print(f"Cache size: {ec.cache_size}")    # 2
