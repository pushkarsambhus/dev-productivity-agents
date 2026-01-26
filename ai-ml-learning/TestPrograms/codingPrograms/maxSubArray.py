class maxSubArray:
    def maxSubArray(self, nums):
        max_current = nums[0]  # Best sum ending at current position
        max_global = nums[0]  # Best sum found so far

        for i in range(1, len(nums)):
            # At each position, decide:
            # 1. Continue the subarray: max_current + nums[i]
            # 2. Start fresh: nums[i]
            # Take the better option
            max_current = max(nums[i], max_current + nums[i])

            # Update global max if current is better
            max_global = max(max_global, max_current)

        return max_global


if __name__ == "__main__":
    sol = maxSubArray()

    #print(sol.maxSubArray([-2, 1, -3, 4, -1, 2, 1, -5, 4]))  # 6
    #print(sol.maxSubArray([-1]))  # -1
    print(sol.maxSubArray([5, 4, -1, 7]))  # 19