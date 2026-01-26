class Solution:
    def threeSum(self, nums):
        nums.sort()  # Sort first
        result = []
        n = len(nums)

        for i in range(n - 2):
            # Skip duplicates
            if i > 0 and nums[i] == nums[i - 1]:
                continue

            # If smallest three numbers sum > 0, no solution
            if nums[i] + nums[i + 1] + nums[i + 2] > 0:
                break

            # Skip if largest possible sum is still negative
            if nums[i] + nums[n - 2] + nums[n - 1] < 0:
                continue

            # Two pointer approach
            left = i + 1
            right = n - 1

            while left < right:
                total = nums[i] + nums[left] + nums[right]

                if total == 0:
                    result.append([nums[i], nums[left], nums[right]])
                    # Skip duplicates
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1
                    left += 1
                    right -= 1
                elif total < 0:
                    left += 1
                else:
                    right -= 1

        return result


if __name__ == "__main__":
    sol = Solution()

    print(sol.threeSum([-1, 0, 1, 2, -1, -4]))  # [[-1, -1, 2], [-1, 0, 1]]
    print(sol.threeSum([0, 0, 0, 0]))  # [[0, 0, 0]]
    print(sol.threeSum([-2, 0, 1, 1, 2]))  # [[-2, 0, 2], [-2, 1, 1]]