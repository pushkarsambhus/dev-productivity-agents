class nextGreaterElement:
    def nextGreaterElement(self, nums):
        n = len(nums)
        result = [-1] * n
        stack = []

        # Traverse right to left
        for i in range(n - 1, -1, -1):
            # Pop elements from stack that are smaller or equal
            while stack and stack[-1] <= nums[i]:
                stack.pop()

            # If stack is not empty, top is the answer
            if stack:
                result[i] = stack[-1]

            # Push current element to stack
            stack.append(nums[i])

        return result


if __name__ == "__main__":
    sol = nextGreaterElement()

    test1 = [1, 3, 2, 4]
    print(sol.nextGreaterElement(test1))
    # Expected: [3, 4, 4, -1]

    test2 = [2, 1, 2, 4]
    print(sol.nextGreaterElement(test2))
    # Expected: [4, 2, 4, -1]

    test3 = [5, 4, 3, 2, 1]
    print(sol.nextGreaterElement(test3))
    # Expected: [-1, -1, -1, -1, -1]