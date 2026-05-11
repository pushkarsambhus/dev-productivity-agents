# Practice: Lambda Functions and Built-in Functions
# In these exercises you will practice: lambda, map(), filter(), sorted(), and zip()

# ===========================================================================
# Problem 1: Lambda to Double a Number
# ===========================================================================
# Use a lambda to create a function that doubles a number.
# Test it with the number 7.

# YOUR CODE HERE

# Expected output:
# 14


# ===========================================================================
# Problem 2: Map with Lambda - Squares
# ===========================================================================
# Given numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
# use map() with a lambda to get their squares and convert to a list.

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# YOUR CODE HERE

# Expected output:
# [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]


# ===========================================================================
# Problem 3: Filter with Lambda - Divisible by 3
# ===========================================================================
# Given numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
# use filter() with a lambda to keep only numbers divisible by 3.

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# YOUR CODE HERE

# Expected output:
# [3, 6, 9]


# ===========================================================================
# Problem 4: Sort by String Length
# ===========================================================================
# Given words = ["banana", "apple", "cherry", "date"],
# use sorted() with a key lambda to sort by string length (shortest first).

words = ["banana", "apple", "cherry", "date"]

# YOUR CODE HERE

# Expected output:
# ['date', 'apple', 'banana', 'cherry']


# ===========================================================================
# Problem 5: Zip and Sort by Age
# ===========================================================================
# Given names = ["Alice", "Bob", "Carol"] and ages = [30, 25, 35],
# use zip() to pair them, then use sorted() with a key lambda to sort
# by age (youngest first). Print each name and age.

names = ["Alice", "Bob", "Carol"]
ages = [30, 25, 35]

# YOUR CODE HERE

# Expected output:
# Bob: 25
# Alice: 30
# Carol: 35


if __name__ == "__main__":
    print("Run the code above each problem to test it!")
    print("Compare your output to the '# Expected output:' comments.")
