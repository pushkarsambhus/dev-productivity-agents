"""
SOLUTION: Phase 4 | LLM / AI Patterns | 02 RAG Basics
"""
import math
from dataclasses import dataclass, field


@dataclass
class Document:
    id: str
    text: str
    metadata: dict = field(default_factory=dict)


@dataclass
class Chunk:
    doc_id: str
    chunk_id: str
    text: str
    embedding: list[float] = field(default_factory=list)


# ── Step 1: Chunking ───────────────────────────────────────────────────────────
def chunk_document(doc: Document, chunk_size: int = 50, overlap: int = 10) -> list[Chunk]:
    words = doc.text.split()
    step = chunk_size - overlap
    chunks = []
    for i, start in enumerate(range(0, len(words), step)):
        window = words[start : start + chunk_size]
        if not window:
            break
        chunks.append(Chunk(
            doc_id=doc.id,
            chunk_id=f"{doc.id}_chunk_{i}",
            text=" ".join(window),
        ))
    return chunks
    # overlap means adjacent chunks share `overlap` words
    # This preserves context across chunk boundaries — important for coherent retrieval


# ── Step 2: Embedding ─────────────────────────────────────────────────────────
def embed_text(text: str, vocab: list[str]) -> list[float]:
    words = text.lower().split()
    counts = [words.count(w) for w in vocab]
    magnitude = math.sqrt(sum(c * c for c in counts))
    if magnitude == 0:
        return [0.0] * len(vocab)
    return [c / magnitude for c in counts]
    # L2 normalization: divide by magnitude so all vectors have length 1
    # This makes cosine similarity equivalent to dot product


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    mag_a = math.sqrt(sum(x * x for x in a))
    mag_b = math.sqrt(sum(x * x for x in b))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)
    # Since we L2-normalize in embed_text, mag_a and mag_b are both 1.0
    # So this simplifies to just the dot product — but we keep the full formula for clarity


# ── Step 3: Vector Store ───────────────────────────────────────────────────────
class SimpleVectorStore:
    def __init__(self, vocab: list[str]):
        self.vocab = vocab
        self.chunks: list[Chunk] = []

    def add_document(self, doc: Document, chunk_size: int = 50, overlap: int = 10):
        chunks = chunk_document(doc, chunk_size, overlap)
        for chunk in chunks:
            chunk.embedding = embed_text(chunk.text, self.vocab)
            self.chunks.append(chunk)

    def search(self, query: str, top_k: int = 3) -> list[tuple[Chunk, float]]:
        query_embedding = embed_text(query, self.vocab)
        scored = [
            (chunk, cosine_similarity(query_embedding, chunk.embedding))
            for chunk in self.chunks
        ]
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]

    def __len__(self):
        return len(self.chunks)


# ── Interview talking points ───────────────────────────────────────────────────
"""
Q: What's wrong with bag-of-words embeddings?
A: They ignore word order and semantics. "dog bites man" == "man bites dog".
   Real systems use dense embeddings (OpenAI ada, sentence-transformers)
   which capture meaning via neural networks.

Q: Why overlap in chunking?
A: If a key fact spans a chunk boundary, non-overlapping chunks might split it.
   Overlap ensures context is preserved. 10-20% overlap is typical.

Q: What are the tradeoffs in chunk size?
A: Small chunks: more precise retrieval, but lose surrounding context.
   Large chunks: more context, but retrieved chunk may contain irrelevant content.
   Typical: 256–512 tokens, tuned per use case.

Q: How would you scale this to 10M documents?
A: Replace SimpleVectorStore with: ChromaDB (local), Pinecone/Weaviate (cloud),
   or pgvector (Postgres). They use HNSW (approximate nearest neighbor) for
   O(log n) search vs our O(n) brute force.
"""

if __name__ == "__main__":
    docs = [
        Document("d1", "Python is a programming language. Python is used for AI and machine learning. "
                        "Python has simple syntax and is very readable. Many data scientists use Python."),
        Document("d2", "LangChain is a framework for building LLM applications. "
                        "It provides tools for RAG retrieval augmented generation. "
                        "LangChain supports many vector databases and embedding models."),
        Document("d3", "Rate limiting controls how many API requests a client can make. "
                        "Token bucket and sliding window are common rate limiting algorithms. "
                        "Rate limiting prevents abuse and ensures fair usage."),
    ]

    vocab = ["python", "langchain", "llm", "rate", "limiting", "ai", "rag",
             "retrieval", "embedding", "vector", "machine", "learning", "api"]

    store = SimpleVectorStore(vocab)
    for doc in docs:
        store.add_document(doc, chunk_size=20, overlap=5)

    print(f"Total chunks stored: {len(store)}\n")

    queries = [
        "how does Python relate to machine learning",
        "what is RAG and how does LangChain help",
        "how do you prevent API abuse",
    ]

    for query in queries:
        print(f"Query: '{query}'")
        results = store.search(query, top_k=2)
        for chunk, score in results:
            print(f"  [{score:.3f}] ({chunk.chunk_id}) {chunk.text[:80]}...")
        print()
