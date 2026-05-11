# String Interview Questions
# Difficulty: Easy → Hard (Principal Engineer level)
# Sources: Google, Meta, Amazon, NVIDIA, Microsoft real interviews + custom problems
# Instructions: Solve each problem, then run this file to verify your output
#
# STATUS:
#   Q1, Q2 — ATTEMPT NOW (concepts covered: strings, slicing, methods)
#   Q3      — Unlock after Concept #5: Dictionaries
#   Q4      — Unlock after Concept #20: Sliding Window
#   Q5      — Unlock after Concept #11: Loops
#   Q6      — Unlock after Concept #23: Recursion
#   Q7      — Unlock after Concept #20: Sliding Window + Concept #21: Hash Maps

# ===========================================================================
# EASY
# ===========================================================================

# Q1: Valid Palindrome [Easy] — Asked at Google, Meta, Amazon, Microsoft
# ---------------------------------------------------------------------------
# Given a string, determine if it is a palindrome considering ONLY alphanumeric
# characters and ignoring case.
# Note: spaces and punctuation are ignored.
#
# Example:
#   "A man, a plan, a canal: Panama" → True
#   "race a car"                     → False
#   " "                              → True (empty after filtering = palindrome)

def is_valid_palindrome(s):
    # YOUR CODE HERE
    cleanedString = [chars.lower() for chars in s if chars.isalnum()]
    return cleanedString == cleanedString[::-1]
    
print(is_valid_palindrome("A man, a plan, a canal: Panama"))  # True
print(is_valid_palindrome("race a car"))                       # False
print(is_valid_palindrome(" "))                                # True


# Q2: Reverse Words in a String [Easy] — Asked at Amazon, Microsoft
# ---------------------------------------------------------------------------
# Given a string, reverse the order of words.
# Words are separated by spaces. Remove extra spaces.
#
# Example:
#   "the sky is blue"   → "blue is sky the"
#   "  hello world  "  → "world hello"
#   "a good   example" → "example good a"

def reverse_words(s):
    reversedList = s.split()
    return " ".join(reversedList[::-1])
    pass

print(reverse_words("the sky is blue"))    # "blue is sky the"
print(reverse_words("  hello world  "))    # "world hello"
print(reverse_words("a good   example"))   # "example good a"


# ===========================================================================
# MEDIUM
# ===========================================================================

# Q3: Group Anagrams [Medium] — Asked at Google, Meta, Amazon, Microsoft
# ---------------------------------------------------------------------------
# Given a list of strings, group the anagrams together.
# Anagrams are words with the same characters in different order.
#
# Example:
#   ["eat","tea","tan","ate","nat","bat"]
#   → [["eat","tea","ate"], ["tan","nat"], ["bat"]]  (order within groups doesn't matter)

def group_anagrams(strs):
    # YOUR CODE HERE
    pass

print(group_anagrams(["eat","tea","tan","ate","nat","bat"]))
# Expected: [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]


# Q4: Longest Substring Without Repeating Characters [Medium] — Asked at Google, Meta, NVIDIA
# ---------------------------------------------------------------------------
# Given a string, find the length of the longest substring
# that contains no repeating characters.
#
# Example:
#   "abcabcbb" → 3  ("abc")
#   "bbbbb"    → 1  ("b")
#   "pwwkew"   → 3  ("wke")

def longest_unique_substring(s):
    # YOUR CODE HERE
    pass

print(longest_unique_substring("abcabcbb"))  # 3
print(longest_unique_substring("bbbbb"))     # 1
print(longest_unique_substring("pwwkew"))    # 3


# Q5: String Compression [Medium] — Asked at Amazon, Google
# ---------------------------------------------------------------------------
# Compress a string using counts of repeated characters.
# If the compressed string is not smaller than the original, return the original.
#
# Example:
#   "aabcccccaaa" → "a2b1c5a3"
#   "abc"         → "abc"  (compressed "a1b1c1" is longer, return original)

def compress_string(s):
    # YOUR CODE HERE
    pass

print(compress_string("aabcccccaaa"))  # "a2b1c5a3"
print(compress_string("abc"))          # "abc"


# ===========================================================================
# HARD (Principal Engineer level)
# ===========================================================================

# Q6: Longest Palindromic Substring [Hard] — Asked at Google, Meta, Amazon
# ---------------------------------------------------------------------------
# Given a string, return the longest substring that is a palindrome.
# If there are multiple of the same length, return the first one found.
#
# Example:
#   "babad" → "bab"  (or "aba", both valid)
#   "cbbd"  → "bb"
#   "a"     → "a"

def longest_palindrome(s):
    # YOUR CODE HERE
    pass

print(longest_palindrome("babad"))  # "bab" or "aba"
print(longest_palindrome("cbbd"))   # "bb"
print(longest_palindrome("a"))      # "a"


# Q7: Minimum Window Substring [Hard] — Asked at Google, Meta, Amazon, Microsoft
# ---------------------------------------------------------------------------
# Given two strings s and t, return the minimum window substring of s
# that contains all characters of t. If no such window exists, return "".
#
# Example:
#   s = "ADOBECODEBANC", t = "ABC" → "BANC"
#   s = "a", t = "a"               → "a"
#   s = "a", t = "aa"              → ""

def min_window(s, t):
    # YOUR CODE HERE
    pass

print(min_window("ADOBECODEBANC", "ABC"))  # "BANC"
print(min_window("a", "a"))                # "a"
print(min_window("a", "aa"))               # ""
