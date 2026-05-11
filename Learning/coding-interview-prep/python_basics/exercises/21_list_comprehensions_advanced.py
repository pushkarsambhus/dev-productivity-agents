# Practice: Advanced List and Dict Comprehensions
# In these exercises you will practice: filtering, nested comprehensions, conditionals, and dict comprehensions

# ===========================================================================
# Problem 1: Filter Words by Length
# ===========================================================================
# Use a list comprehension to get all words longer than 4 characters
# from "the quick brown fox jumps over the lazy dog".

# YOUR CODE HERE

# Expected output:
# ['quick', 'brown', 'jumps', 'over']


# ===========================================================================
# Problem 2: Flatten Nested List
# ===========================================================================
# Use a nested list comprehension to flatten [[1,2,3],[4,5,6],[7,8,9]]
# into [1,2,3,4,5,6,7,8,9].

# YOUR CODE HERE

# Expected output:
# [1, 2, 3, 4, 5, 6, 7, 8, 9]


# ===========================================================================
# Problem 3: Conditional Labels
# ===========================================================================
# Use a list comprehension with inline if/else to label each number in 1-10
# as "even" or "odd".

# YOUR CODE HERE

# Expected output:
# ['odd', 'even', 'odd', 'even', 'odd', 'even', 'odd', 'even', 'odd', 'even']


# ===========================================================================
# Problem 4: Create Multiplication Table
# ===========================================================================
# Create a 5x5 multiplication table using a nested list comprehension.
# Result should be a list of lists where each inner list is a row.

# YOUR CODE HERE

# Expected output:
# [[1, 2, 3, 4, 5],
#  [2, 4, 6, 8, 10],
#  [3, 6, 9, 12, 15],
#  [4, 8, 12, 16, 20],
#  [5, 10, 15, 20, 25]]


# ===========================================================================
# Problem 5: Invert Dictionary
# ===========================================================================
# Use a dict comprehension to invert a dictionary.
# Transform {"a":1, "b":2, "c":3} into {1:"a", 2:"b", 3:"c"}

# YOUR CODE HERE

# Expected output:
# {1: 'a', 2: 'b', 3: 'c'}


if __name__ == "__main__":
    print("Run the code above each problem to test it!")
    print("Compare your output to the '# Expected output:' comments.")
