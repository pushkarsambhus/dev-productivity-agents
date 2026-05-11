# Practice: Sets
# In these exercises you will practice: set creation, operations (union, intersection, difference), and membership

# ===========================================================================
# Problem 1: Remove Duplicates with Sets
# ===========================================================================
# Given numbers = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4],
# use a set to find all unique numbers and print them.

numbers = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]

# YOUR CODE HERE

# Expected output:
# {1, 2, 3, 4}


# ===========================================================================
# Problem 2: Set Operations - Union, Intersection, Difference
# ===========================================================================
# Given a = {1, 2, 3, 4, 5} and b = {4, 5, 6, 7, 8}, print:
# 1) Union (all elements from both sets)
# 2) Intersection (elements in both sets)
# 3) Difference a - b (in a but not in b)
# 4) Symmetric difference (in either but not both)

a = {1, 2, 3, 4, 5}
b = {4, 5, 6, 7, 8}

# YOUR CODE HERE

# Expected output:
# Union: {1, 2, 3, 4, 5, 6, 7, 8}
# Intersection: {4, 5}
# Difference (a - b): {1, 2, 3}
# Symmetric difference: {1, 2, 3, 6, 7, 8}


# ===========================================================================
# Problem 3: Find Students in Both Classes
# ===========================================================================
# Given two lists of student names (class A and class B),
# find:
# 1) Students in both classes
# 2) Students only in class A
# 3) Students in either class

class_a = ["Alice", "Bob", "Charlie", "Diana"]
class_b = ["Bob", "Diana", "Eve", "Frank"]

# YOUR CODE HERE

# Expected output:
# In both classes: {'Bob', 'Diana'}
# Only in class A: {'Alice', 'Charlie'}
# In either class: {'Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank'}


# ===========================================================================
# Problem 4: Subset Checking
# ===========================================================================
# Check if {1, 2, 3} is a subset of {1, 2, 3, 4, 5}.
# Check if {1, 2, 6} is a subset of {1, 2, 3, 4, 5}.
# Print results for each.

# YOUR CODE HERE

# Expected output:
# {1, 2, 3} is subset of {1, 2, 3, 4, 5}: True
# {1, 2, 6} is subset of {1, 2, 3, 4, 5}: False


# ===========================================================================
# Problem 5: Count Unique Characters in a String
# ===========================================================================
# Given the string "mississippi",
# use a set to find how many unique characters it contains.
# Print both the count and the unique characters.

word = "mississippi"

# YOUR CODE HERE

# Expected output:
# Unique characters: 4
# Characters: {'m', 'i', 's', 'p'}


if __name__ == "__main__":
    print("Run the code above each problem to test it!")
    print("Compare your output to the '# Expected output:' comments.")
