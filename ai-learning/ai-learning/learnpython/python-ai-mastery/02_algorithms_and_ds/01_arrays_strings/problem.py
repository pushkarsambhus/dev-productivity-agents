"""
PHASE 2 | ALGORITHMS & DS | 01 ARRAYS & STRINGS
================================================
Topic: Sliding window, two pointers, string manipulation.
~30% of interview problems use these patterns.
"""

# ── Problem 1: Sliding Window — Max Avg Chunk Score ───────────────────────────
# In RAG systems, you retrieve chunks and score them. Given a list of chunk
# scores and a window size k, find the maximum average score of any k consecutive chunks.
#
# Example: scores=[0.8, 0.6, 0.9, 0.7, 0.5], k=3 → 0.73  (0.8+0.6+0.9)/3
# Brute force: O(n*k) — recompute sum each window
# Optimal: O(n) — slide the window, add new, drop old

def max_avg_chunk_score(scores: list[float], k: int) -> float:
    pass


# ── Problem 2: Two Pointers — Valid Token Pair ────────────────────────────────
# Given a sorted list of token counts and a target, determine if any TWO
# token counts sum to the target.
# (Two Sum variant — but sorted, so two pointers beats hashmap in space)
#
# Example: counts=[100, 300, 500, 700, 900], target=1200 → True (300+900)

def has_token_pair(counts: list[int], target: int) -> bool:
    pass


# ── Problem 3: String — Truncate to Token Limit ───────────────────────────────
# A simple but practical one: given a string and a max_tokens limit,
# truncate the string to at most max_tokens words (split on whitespace).
# Return the truncated string. If already within limit, return as-is.
#
# Example: ("The quick brown fox jumps", 3) → "The quick brown"

def truncate_to_tokens(text: str, max_tokens: int) -> str:
    pass


# ── Problem 4: Sliding Window — Longest Context Window ────────────────────────
# Given a string of tokens (space-separated), find the length of the longest
# substring (contiguous sequence of tokens) with no repeated tokens.
# This models finding the longest non-repeating context window.
#
# Example: "embed chunk embed index chunk retrieve" → 4 (chunk embed index chunk? no)
# Tokens: [embed, chunk, embed, index, chunk, retrieve]
# Answer: 4 → "chunk embed index chunk"? No — "embed index chunk retrieve" = 4 unique
# Hint: use a set + two pointers (left, right)

def longest_unique_window(token_string: str) -> int:
    pass


# ── Self-check ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(max_avg_chunk_score([0.8, 0.6, 0.9, 0.7, 0.5], 3))   # 0.73
    print(max_avg_chunk_score([1.0, 0.9, 0.8, 0.7], 2))         # 0.95

    print(has_token_pair([100, 300, 500, 700, 900], 1200))       # True
    print(has_token_pair([100, 300, 500, 700, 900], 999))        # False

    print(truncate_to_tokens("The quick brown fox jumps", 3))    # "The quick brown"
    print(truncate_to_tokens("Short", 10))                        # "Short"

    print(longest_unique_window("embed chunk embed index chunk retrieve"))  # 4
    print(longest_unique_window("a b c d"))                                  # 4
    print(longest_unique_window("a a a"))                                    # 1
