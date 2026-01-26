"""
06_embedding_search.py
----------------------
Goal: Build a tiny in‑memory "embedding index" and run nearest‑neighbor search using cosine similarity.

Why this matters:
- Retrieval and similarity search are core to GenAI (RAG).
- You'll show ability to combine data structures with vector math.
"""

from typing import List, Tuple
from math import sqrt

def cosine(a: List[float], b: List[float]) -> float:
    dot = sum(x*y for x, y in zip(a, b))
    mag_a = sqrt(sum(x*x for x in a))
    mag_b = sqrt(sum(y*y for y in b))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)

class EmbeddingIndex:
    def __init__(self):
        self._items: List[Tuple[str, List[float]]] = []  # (id, vector)

    def add(self, item_id: str, vector: List[float]) -> None:
        # Defensive copy to avoid accidental external mutation
        self._items.append((str(item_id), list(map(float, vector))))

    def search(self, query: List[float], k: int = 3) -> List[Tuple[str, float]]:
        # Compute similarities and return top-k by score
        scored = []
        for item_id, vec in self._items:
            scored.append((item_id, cosine(query, vec)))
        # Sort descending by similarity
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:k]


if __name__ == "__main__":
    idx = EmbeddingIndex()
    idx.add("doc-A", [1, 0, 0])
    idx.add("doc-B", [0.7, 0.7, 0])
    idx.add("doc-C", [0, 1, 0])
    results = idx.search([0.9, 0.1, 0], k=2)
    print("Top-2:", results)
