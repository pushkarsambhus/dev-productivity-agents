"""
SOLUTION: Phase 2 | Algorithms & DS | 02 Hashmaps & Sets
"""
from collections import defaultdict

# ── Problem 1: Two Sum ─────────────────────────────────────────────────────────
def two_sum(nums: list[int], target: int) -> list[int]:
    seen = {}  # maps value → index
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
    # WHY this works: for each number, we ask "have I seen what I need to reach target?"
    # One pass, O(n) time, O(n) space.
    # Pattern: "store what you've seen, look up what you need"


# ── Problem 2: Frequency Counter ──────────────────────────────────────────────
def char_frequency(s: str) -> dict:
    counts = defaultdict(int)
    for ch in s:
        if ch != " ":
            counts[ch] += 1
    # Sort by count descending — sorted() returns a list of tuples
    return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))
    # key=lambda x: x[1] means "sort by the second element (the count)"
    # This lambda pattern is everywhere in Python — memorize it.


# ── Problem 3: Group Anagrams ──────────────────────────────────────────────────
def group_anagrams(strs: list[str]) -> list[list[str]]:
    groups = defaultdict(list)
    for word in strs:
        key = tuple(sorted(word))   # "eat" → ('a','e','t')
        groups[key].append(word)
    return list(groups.values())
    # Key insight: sorted chars = canonical form = hashable key
    # tuple() is needed because lists can't be dict keys (not hashable)


# ── Problem 4: LLM Cache Hit Rate ─────────────────────────────────────────────
def cache_hit_rate(prompt_hashes: list[str]) -> float:
    seen = set()
    hits = 0
    for h in prompt_hashes:
        if h in seen:
            hits += 1
        seen.add(h)
    return round(hits / len(prompt_hashes), 2)
    # Set lookup is O(1) — sets are hashmaps without values
    # This exact pattern appears in semantic cache implementations


if __name__ == "__main__":
    print(two_sum([2, 7, 11, 15], 9))       # [0, 1]
    print(two_sum([3, 2, 4], 6))             # [1, 2]
    print(char_frequency("hello world"))
    print(group_anagrams(["eat","tea","tan","ate","nat","bat"]))
    print(cache_hit_rate(["abc","xyz","abc","abc","def"]))  # 0.4
