"""
SOLUTION: Phase 3 | System Design Coding | 02 Caching (LRU Cache)
"""
from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()
        # OrderedDict maintains insertion order.
        # Convention: FRONT = least recently used, END = most recently used.

    def get(self, key: str) -> any:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)   # mark as most recently used
        return self.cache[key]

    def put(self, key: str, value: any):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)   # last=False → pop from FRONT (LRU)
            # last=True would pop from end (most recent) — the opposite of what we want

    def __repr__(self):
        return f"LRUCache({dict(self.cache)})"


# ── Interview talking point ────────────────────────────────────────────────────
"""
Q: Why OrderedDict over a regular dict?
A: Regular dicts (Python 3.7+) maintain insertion order but have no move_to_end().
   OrderedDict adds that in O(1) via a doubly linked list under the hood.

Q: What if you couldn't use OrderedDict?
A: Implement a doubly linked list + hash map manually.
   - Hash map: key → node (O(1) access)
   - Doubly linked list: maintains order, O(1) move to front/back
   This is the "hard" version of this problem on LeetCode (#146).

Q: Where does this appear in production AI systems?
A: - Semantic caches (GPTCache, LangChain's InMemoryCache)
   - Embedding caches to avoid re-calling OpenAI/Anthropic APIs
   - KV cache in transformer inference (different concept, same name)
"""


class EmbeddingCache:
    def __init__(self, embed_fn: callable, capacity: int = 500):
        self.embed_fn = embed_fn
        self._cache = LRUCache(capacity)
        self._size = 0

    def embed(self, text: str) -> list[float]:
        cached = self._cache.get(text)
        if cached != -1:
            return cached                    # cache hit
        embedding = self.embed_fn(text)
        self._cache.put(text, embedding)
        self._size += 1
        return embedding

    @property
    def cache_size(self) -> int:
        return len(self._cache.cache)


if __name__ == "__main__":
    print("=== LRU Cache ===")
    cache = LRUCache(capacity=3)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("c", 3)
    print(cache.get("a"))
    cache.put("d", 4)
    print(cache.get("b"))    # -1
    print(cache.get("c"))    # 3
    print(cache.get("d"))    # 4
    print(cache)

    print("\n=== Embedding Cache ===")
    call_count = 0

    def fake_embed(text: str) -> list[float]:
        global call_count
        call_count += 1
        return [len(text) * 0.01, 0.5]

    ec = EmbeddingCache(fake_embed, capacity=10)
    ec.embed("hello world")
    ec.embed("hello world")
    ec.embed("different text")
    print(f"API calls made: {call_count}")   # 2
    print(f"Cache size: {ec.cache_size}")    # 2
