class TwoSum:
    def twoSum(self, nums, target):
        # Your code here
        result = []
        seen ={}

        for i in range(len(nums)):
            complement = target - nums[i]

            if complement in seen:
                return [seen[complement], i]

            seen[nums[i]] = i

        return []


if __name__ == "__main__":
    sol = TwoSum()

    #print(sol.twoSum([2, 7, 11, 15], 9))  # [0, 1]
    #print(sol.twoSum([3, 2, 4], 6))  # [1, 2]
    #print(sol.twoSum([3, 3], 6))  # [0, 1]
    print(sol.twoSum([1, 5, 3, 7], 8))  # [0, 1]
    print(sol.twoSum([2, 7, 11, 15], 9))  # [0, 1]
    print(sol.twoSum([3, 2, 4], 6))  # [1, 2]
    print(sol.twoSum([3, 3], 6))  # [0, 1]