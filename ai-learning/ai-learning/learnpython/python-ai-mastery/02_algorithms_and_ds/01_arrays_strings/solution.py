"""
SOLUTION: Phase 2 | Algorithms & DS | 01 Arrays & Strings
"""

# ── Problem 1: Sliding Window ─────────────────────────────────────────────────
def max_avg_chunk_score(scores: list[float], k: int) -> float:
    # Build first window
    window_sum = sum(scores[:k])
    best = window_sum

    # Slide: add right element, drop left element
    for i in range(k, len(scores)):
        window_sum += scores[i] - scores[i - k]
        best = max(best, window_sum)

    return round(best / k, 2)
    # Key insight: instead of recomputing sum(window), just adjust by +new -dropped
    # This brings O(n*k) → O(n)


# ── Problem 2: Two Pointers ───────────────────────────────────────────────────
def has_token_pair(counts: list[int], target: int) -> bool:
    left, right = 0, len(counts) - 1
    while left < right:
        total = counts[left] + counts[right]
        if total == target:
            return True
        if total < target:
            left += 1    # sum too small → move left pointer right (bigger value)
        else:
            right -= 1   # sum too big  → move right pointer left (smaller value)
    return False
    # Works because list is sorted: we can reason about direction
    # O(n) time, O(1) space — better than hashmap's O(n) space


# ── Problem 3: Truncate ───────────────────────────────────────────────────────
def truncate_to_tokens(text: str, max_tokens: int) -> str:
    words = text.split()
    return " ".join(words[:max_tokens])
    # list[:n] is safe even if n > len(list) — no IndexError
    # " ".join() is idiomatic for reassembling tokens


# ── Problem 4: Longest Unique Window ─────────────────────────────────────────
def longest_unique_window(token_string: str) -> int:
    tokens = token_string.split()
    seen = set()
    left = 0
    best = 0

    for right in range(len(tokens)):
        # Shrink window from left until no duplicate
        while tokens[right] in seen:
            seen.remove(tokens[left])
            left += 1
        seen.add(tokens[right])
        best = max(best, right - left + 1)

    return best
    # Pattern: expand right freely, shrink left only when constraint violated
    # This is the canonical "sliding window with set" template


if __name__ == "__main__":
    print(max_avg_chunk_score([0.8, 0.6, 0.9, 0.7, 0.5], 3))   # 0.73
    print(max_avg_chunk_score([1.0, 0.9, 0.8, 0.7], 2))         # 0.95
    print(has_token_pair([100, 300, 500, 700, 900], 1200))       # True
    print(has_token_pair([100, 300, 500, 700, 900], 999))        # False
    print(truncate_to_tokens("The quick brown fox jumps", 3))
    print(truncate_to_tokens("Short", 10))
    print(longest_unique_window("embed chunk embed index chunk retrieve"))  # 4
    print(longest_unique_window("a b c d"))                                  # 4
    print(longest_unique_window("a a a"))                                    # 1
