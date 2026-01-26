class lengthOfLongestSubstring:
    def lengthOfLongestSubstring(self, s):
        # 1. Track characters in current window using a SET
        char_index = {}
        left = 0
        max_length = 0

        for right in range(len(s)):
            # If char seen before, move left pointer
            if s[right] in char_index:
                # Jump to after the previous occurrence
                left = max(left, char_index[s[right]] + 1)

            # Update last seen index
            char_index[s[right]] = right

            # Update max length
            max_length = max(max_length, right - left + 1)

        return max_length


if __name__ == "__main__":
    sol = lengthOfLongestSubstring()

    print(sol.lengthOfLongestSubstring("abcabcbb"))  # 3
    print(sol.lengthOfLongestSubstring("bbbbb"))  # 1
    print(sol.lengthOfLongestSubstring("pwwkew"))  # 3
    print(sol.lengthOfLongestSubstring(" "))  # 1
    print(sol.lengthOfLongestSubstring("au"))  # 2