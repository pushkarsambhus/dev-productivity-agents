"""
SOLUTION: Phase 5 | Interview Problems | 01 Easy
"""
from collections import Counter


def fizzbuzz(n: int) -> list[str]:
    result = []
    for i in range(1, n + 1):
        if i % 15 == 0:      # check 15 first — avoids checking 3 and 5 separately
            result.append("FizzBuzz")
        elif i % 3 == 0:
            result.append("Fizz")
        elif i % 5 == 0:
            result.append("Buzz")
        else:
            result.append(str(i))
    return result


def reverse_string(s: str) -> str:
    chars = list(s)
    left, right = 0, len(chars) - 1
    while left < right:
        chars[left], chars[right] = chars[right], chars[left]
        left += 1
        right -= 1
    return "".join(chars)
    # In an actual interview: return s[::-1] is fine.
    # Two pointers version shows you know the algorithm.


def count_vowels(s: str) -> int:
    return sum(1 for ch in s.lower() if ch in "aeiou")


def is_palindrome(s: str) -> bool:
    cleaned = "".join(ch.lower() for ch in s if ch.isalnum())
    return cleaned == cleaned[::-1]
    # isalnum() filters to letters and digits only


def find_duplicates(items: list) -> list:
    seen = set()
    dupes = []
    reported = set()
    for item in items:
        if item in seen and item not in reported:
            dupes.append(item)
            reported.add(item)
        seen.add(item)
    return dupes


def flatten_one_level(nested: list) -> list:
    return [item for sublist in nested
            for item in (sublist if isinstance(sublist, list) else [sublist])]
    # isinstance check: if element is a list, iterate it; otherwise wrap in [x]


def running_average(nums: list[float]) -> list[float]:
    result = []
    total = 0.0
    for i, n in enumerate(nums, 1):
        total += n
        result.append(round(total / i, 10))   # enough precision
    return result


def most_common(items: list):
    return Counter(items).most_common(1)[0][0]
    # Counter(items) → {item: count, ...}
    # .most_common(1) → [(item, count)] for top 1
    # [0][0] → the item itself


if __name__ == "__main__":
    print(fizzbuzz(15))
    print(reverse_string("hello"))
    print(count_vowels("hello world"))
    print(is_palindrome("A man a plan a canal Panama"))
    print(find_duplicates([1,2,3,2,4,1,5]))
    print(flatten_one_level([[1,2],[3,[4,5]],6]))
    print(running_average([1,2,3,4]))
    print(most_common([1,2,2,3,3,3,1]))
