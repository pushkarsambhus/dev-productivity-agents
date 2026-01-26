class containsDuplicate:
    def containsDuplicate(self, nums):
        # Your code here
        checkDuplicates = {}

        for num in nums:

            if num in checkDuplicates:
                return True
            else:
                checkDuplicates[num] = 1

        return False

if __name__ == "__main__":
    sol = containsDuplicate()

    print(sol.containsDuplicate([1, 2, 3, 1]))  # True
    print(sol.containsDuplicate([1, 2, 3, 4]))  # False
    print(sol.containsDuplicate([99, 99]))  # True