# Practice: Generators
# In these exercises you will practice: generator functions, yield, and lazy evaluation

# ===========================================================================
# Problem 1: Countdown Generator
# ===========================================================================
# Write a generator countdown(n) that yields n, n-1, n-2, ... 1, 0.
# Print all values for countdown(5).

# YOUR CODE HERE

# Expected output:
# 5
# 4
# 3
# 2
# 1
# 0


# ===========================================================================
# Problem 2: Fibonacci Generator
# ===========================================================================
# Write a generator fibonacci() that yields Fibonacci numbers forever.
# Print the first 10 Fibonacci numbers.

# YOUR CODE HERE

# Expected output:
# 0
# 1
# 1
# 2
# 3
# 5
# 8
# 13
# 21
# 34


# ===========================================================================
# Problem 3: Read Large File Line by Line
# ===========================================================================
# Write a generator read_large_file(filepath) that yields one line at a time.
# This is memory-efficient for very large files.
# Create a test file and use the generator to read it.

# YOUR CODE HERE

# Expected output:
# Line 1
# Line 2
# Line 3


# ===========================================================================
# Problem 4: Generator Expression - Even Squares
# ===========================================================================
# Write a generator expression that yields the square of each even number
# from 1 to 20. Convert to list and print.

# YOUR CODE HERE

# Expected output:
# [4, 16, 36, 64, 100, 144, 196, 256, 324, 400]


# ===========================================================================
# Problem 5: Batch Generator
# ===========================================================================
# Write a generator batch(iterable, size) that yields chunks of size items.
# Example: batch([1..10], 3) yields [1,2,3], [4,5,6], [7,8,9], [10]
# Test with a list of 10 numbers and batch size 3.

# YOUR CODE HERE

# Expected output:
# [1, 2, 3]
# [4, 5, 6]
# [7, 8, 9]
# [10]


if __name__ == "__main__":
    print("Run the code above each problem to test it!")
    print("Compare your output to the '# Expected output:' comments.")
