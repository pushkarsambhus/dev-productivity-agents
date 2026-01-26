from typing import List
from collections import Counter
import heapq


class topKFrequent:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        """
        Find k most frequent elements.

        Approach 1: Using heap (good for k << n)
        - Count frequencies
        - Use min heap of size k
        - Keep top k elements

        Complexity:
        - Time: O(n log k)
        - Space: O(n) for counter, O(k) for heap
        """
        # Step 1: Count frequencies
        count = Counter(nums)

        # Step 2: Use min heap to keep top k
        # heapq.nsmallest(k, ...) keeps smallest k items
        # We want largest k, so negate or use nlargest

        # Method 1: Using nlargest (clean but O(n log k) anyway)
        return heapq.nlargest(k, count.keys(), key=count.get)

sol = topKFrequent()

# Test 1
result1 = sol.topKFrequent([1,1,1,2,2,3], k=2)
print(result1)  # Expected: [1, 2] or [2, 1]

# Test 2
result2 = sol.topKFrequent([1], k=1)
print(result2)  # Expected: [1]

# Test 3
result3 = sol.topKFrequent([4,1,1,1,2,2,3], k=2)
print(result3)  # Expected: [1, 2]