"""
PHASE 4 | LLM / AI PATTERNS | 02 RAG BASICS
============================================
Topic: Build a minimal RAG pipeline from scratch — no LangChain, no vector DB.
Understanding the primitives makes you dangerous in interviews.

RAG = Retrieve → Augment → Generate
1. Chunk documents
2. Embed chunks (convert to vectors)
3. Store vectors
4. At query time: embed query, find similar chunks, pass to LLM

This file implements steps 1-3 using only stdlib + simple math.
No API keys needed — embeddings are faked with a bag-of-words approach.
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
    """
    Split document text into overlapping word-level chunks.

    Args:
        doc: the document to chunk
        chunk_size: words per chunk
        overlap: words shared between adjacent chunks

    TODO:
    1. Split doc.text into words
    2. Slide a window of size chunk_size, stepping by (chunk_size - overlap)
    3. Each window becomes a Chunk with chunk_id = f"{doc.id}_chunk_{i}"
    """
    pass


# ── Step 2: Embedding (simplified) ────────────────────────────────────────────
def embed_text(text: str, vocab: list[str]) -> list[float]:
    """
    Bag-of-words embedding: returns a vector of word frequencies, normalized.
    In production: call OpenAI/Anthropic embeddings API here.

    TODO:
    1. Lowercase and split text into words
    2. For each word in vocab, count how many times it appears in text
    3. Return L2-normalized vector (divide each value by the vector's magnitude)
    4. If zero vector (no vocab words found), return all zeros
    """
    pass


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """
    Similarity between two vectors. 1.0 = identical direction, 0.0 = orthogonal.
    TODO: dot(a,b) / (magnitude(a) * magnitude(b))
    Return 0.0 if either vector is all zeros.
    """
    pass


# ── Step 3: Vector Store ───────────────────────────────────────────────────────
class SimpleVectorStore:
    """
    In-memory vector store. In production: ChromaDB, Pinecone, pgvector.
    """

    def __init__(self, vocab: list[str]):
        self.vocab = vocab
        self.chunks: list[Chunk] = []

    def add_document(self, doc: Document, chunk_size: int = 50, overlap: int = 10):
        """Chunk, embed, and store a document."""
        # TODO: chunk the doc, embed each chunk, store in self.chunks
        pass

    def search(self, query: str, top_k: int = 3) -> list[tuple[Chunk, float]]:
        """
        Return top_k most similar chunks to query.
        TODO:
        1. Embed the query
        2. Compute cosine similarity against every stored chunk
        3. Sort by similarity descending, return top_k (chunk, score) pairs
        """
        pass

    def __len__(self):
        return len(self.chunks)


# ── Self-check ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Build a tiny knowledge base
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
