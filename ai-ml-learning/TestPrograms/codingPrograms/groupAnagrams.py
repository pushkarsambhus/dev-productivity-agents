from collections import defaultdict

class groupAnagrams:
    def groupAnagrams(self, strs):
        # Your code here
        groups = defaultdict(list)
        for word in strs:
            sorted_word = ''.join(sorted(word))
            groups[sorted_word].append(word)

        return list(groups.values())
        pass


if __name__ == "__main__":
    sol = groupAnagrams()

    print(sol.groupAnagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))
    # [["bat"],["nat","tan"],["ate","eat","tea"]] (order may vary)

    print(sol.groupAnagrams([""]))
    # [[""]]

    print(sol.groupAnagrams(["a"]))
    # [["a"]]