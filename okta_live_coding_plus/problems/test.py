"""
100% Free RAG system - no API costs!
"""
from sentence_transformers import SentenceTransformer, CrossEncoder
import chromadb

# Step 1: Initialize (all runs locally, no API key)
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')  # For better results

vector_db = chromadb.Client()
collection = vector_db.create_collection("documents")

# Step 2: Add documents (same as before)
def add_document(text, doc_id):
    """Store document in vector database"""
    embedding = embedding_model.encode(text).tolist()
    
    collection.add(
        embeddings=[embedding],
        documents=[text],
        ids=[doc_id]
    )
    print(f"Added document {doc_id}")

# Step 3: Search with reranking
def search_documents(query, top_k=3):
    """Find most relevant documents"""
    query_embedding = embedding_model.encode(query).tolist()
    
    # Get more candidates for reranking
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k * 2
    )
    
    documents = results['documents'][0]
    
    # Rerank for better quality
    pairs = [[query, doc] for doc in documents]
    scores = reranker.predict(pairs)
    
    # Sort by score and return top k
    ranked_docs = sorted(zip(documents, scores), key=lambda x: x[1], reverse=True)
    return [doc for doc, score in ranked_docs[:top_k]]

# Step 4: Free answer generation (extractive QA)
def rag_query_free(question):
    """Answer question without API costs"""
    # Retrieve relevant docs
    relevant_docs = search_documents(question, top_k=3)
    
    if not relevant_docs:
        return "No relevant information found."
    
    # Simple extractive answer - return most relevant document
    context = "\n\n".join(relevant_docs)
    
    return f"Based on the documents:\n\n{relevant_docs[0]}\n\n(This is the most relevant information found)"

# For better answers with a local LLM (still free)
def rag_query_with_local_llm(question):
    """Use a local LLM for free"""
    try:
        # Option 1: Use Ollama (install separately)
        import ollama
        
        relevant_docs = search_documents(question, top_k=3)
        context = "\n\n".join(relevant_docs)
        
        response = ollama.chat(
            model='llama3.2',  # or 'mistral', 'phi'
            messages=[
                {
                    'role': 'system',
                    'content': 'Answer based only on the provided context.'
                },
                {
                    'role': 'user',
                    'content': f'Context:\n{context}\n\nQuestion: {question}'
                }
            ]
        )
        
        return response['message']['content']
    
    except ImportError:
        return rag_query_free(question)

# Example usage
if __name__ == "__main__":
    # Add documents
    add_document("Python is a high-level programming language.", "doc1")
    add_document("Machine learning is a subset of AI.", "doc2")
    add_document("Vector databases enable similarity search.", "doc3")
    add_document("Python was created by Guido van Rossum in 1991.", "doc4")
    
    # Ask questions - COMPLETELY FREE
    print("=" * 50)
    answer = rag_query_free("What is Python?")
    print(answer)
    print("=" * 50)
    
    # Cost: $0.00