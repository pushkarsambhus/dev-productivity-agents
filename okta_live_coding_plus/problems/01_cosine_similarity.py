"""
01_cosine_similarity.py
-----------------------
Goal: Compute cosine similarity between two vectors.

Why this matters:
- Used in information retrieval, embeddings, and vector search.
- Interviewers often check basic linear‑algebra reasoning + robust input handling.

We use only the Python standard library so you can run it anywhere.
"""

from math import sqrt
from typing import List

def cosine_similarity(a: List[float], b: List[float]) -> float:
    """
    Compute cosine similarity between vectors a and b.

    Cosine similarity = (a · b) / (||a|| * ||b||)
    - a · b is the dot product (sum of element‑wise products).
    - ||a|| is the magnitude (square root of sum of squares).

    We include **defensive checks** so you can safely call this function:
    - Vectors must be the same length.
    - They cannot be empty.
    - If either vector is all zeros, similarity is defined as 0.0 to avoid division by zero.
    """
    if not isinstance(a, list) or not isinstance(b, list):
        raise TypeError("Inputs must be lists of numbers.")
    if len(a) != len(b):
        raise ValueError("Vectors must be the same length.")
    if len(a) == 0:
        raise ValueError("Vectors must not be empty.")

    # Compute dot product: sum(a[i] * b[i])
    dot = 0.0
    for x, y in zip(a, b):
        dot += float(x) * float(y)

    # Compute magnitudes: sqrt(sum(x^2))
    mag_a = sqrt(sum(float(x) * float(x) for x in a))
    mag_b = sqrt(sum(float(y) * float(y) for y in b))

    # If either vector has zero magnitude, define similarity as 0 (no direction)
    if mag_a == 0.0 or mag_b == 0.0:
        return 0.0

    return dot / (mag_a * mag_b)


if __name__ == "__main__":
    # Demo: three quick examples
    v1 = [1, 0, 0]
    v2 = [0, 1, 0]
    v3 = [1, 1, 0]
    v4 = [0, 0, 'abc']
    print("cos(v1, v2) ->", round(cosine_similarity(v1, v2), 4))  # Orthogonal -> 0.0
    print("cos(v1, v1) ->", round(cosine_similarity(v1, v1), 4))  # Identical -> 1.0
    print("cos(v1, v3) ->", round(cosine_similarity(v1, v3), 4))  # Angle between -> ~0.7071
    print("cos(v1, v4) ->", round(cosine_similarity(v1, v4), 4))  # Type error -> ValueError    