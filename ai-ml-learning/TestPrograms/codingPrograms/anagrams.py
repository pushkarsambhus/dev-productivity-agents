from typing import Counter


class isAnagram:
    def isAnagram(self, s, t):
        # Your code here
        s_count = Counter(s)
        t_count = Counter(t)

        if s_count == t_count:
            return True

        return False


if __name__ == "__main__":
    sol = isAnagram()

    print(sol.isAnagram("anagram", "nagaram"))  # True
    print(sol.isAnagram("rat", "car"))  # False
    print(sol.isAnagram("ab", "ba"))  # True
    print(sol.isAnagram("ab", "a"))  # False