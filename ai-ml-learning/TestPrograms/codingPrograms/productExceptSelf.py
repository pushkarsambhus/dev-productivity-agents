class productExceptSelf:
    def productExceptSelf(self, nums):
        n = len(nums)
        left = [1] * n
        right = [1] * n

        print(f"Input: {nums}\n")

        # Pass 1: Fill left array (left to right)
        print("=== PASS 1: Building LEFT array ===")
        for i in range(1, n):
            left[i] = left[i - 1] * nums[i - 1]
            print(f"i={i}: left[{i}] = left[{i - 1}] * nums[{i - 1}] = {left[i - 1]} * {nums[i - 1]} = {left[i]}")
        print(f"Left array: {left}\n")

        # Pass 2: Fill right array (right to left)
        print("=== PASS 2: Building RIGHT array ===")
        for i in range(n - 2, -1, -1):
            right[i] = right[i + 1] * nums[i + 1]
            print(f"i={i}: right[{i}] = right[{i + 1}] * nums[{i + 1}] = {right[i + 1]} * {nums[i + 1]} = {right[i]}")
        print(f"Right array: {right}\n")

        # Pass 3: Combine left and right
        print("=== PASS 3: Combining LEFT * RIGHT ===")
        result = []
        for i in range(n):
            product = left[i] * right[i]
            result.append(product)
            print(f"i={i}: result[{i}] = left[{i}] * right[{i}] = {left[i]} * {right[i]} = {product}")

        print(f"\nFinal result: {result}")
        return result


if __name__ == "__main__":
    sol = productExceptSelf()

    print(sol.productExceptSelf([1, 2, 3, 4]))  # [24,12,8,6]
    print(sol.productExceptSelf([-1, 1, 0, -3, 3]))  # [0,0,9,0,0]