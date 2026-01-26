from typing import List

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        h = {}
        for i,num in enumerate(nums):
            h[num] = i
        
        for i, num in enumerate(nums):
            desired = target - num
            if desired in h and h[desired] != i:
                return i , h[desired]


if __name__ == "__main__":
    solution = Solution()
    
    # Add your test cases here
    result = solution.twoSum([3,2,4], 6)
    print(f"Result: {result}")