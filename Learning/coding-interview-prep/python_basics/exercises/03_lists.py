# Practice: Lists
# In these exercises you will practice: list creation, manipulation, slicing, comprehension, and built-in functions

# ===========================================================================
# Problem 1: Add and Insert List Elements
# ===========================================================================
# Create a list of 5 fruits. Add "mango" at the end, insert "kiwi" at index 2,
# then print the final list.

fruits = ["apple", "banana", "cherry", "date", "elderberry"]

# YOUR CODE HERE
fruits.append("mango")
fruits.insert(2,"kiwi")
print(fruits)

# Expected output:
# ['apple', 'banana', 'kiwi', 'cherry', 'date', 'elderberry', 'mango']


# ===========================================================================
# Problem 2: List Functions - Sort, Max, Min, Sum
# ===========================================================================
# Given numbers = [5, 2, 8, 1, 9, 3, 7, 4, 6], print:
# 1) The sorted list
# 2) The maximum value
# 3) The minimum value
# 4) The sum

numbers = [5, 2, 8, 1, 9, 3, 7, 4, 6]

# YOUR CODE HERE
numbers.sort()
print(f"Sorted: {numbers}")
print(f"Max: {max(numbers)}")
print(f"Min: {min(numbers)}")
print(f"Sum: {sum(numbers)}")

# Expected output:
# Sorted: [1, 2, 3, 4, 5, 6, 7, 8, 9]
# Max: 9
# Min: 1
# Sum: 45


# ===========================================================================
# Problem 3: List Slicing and Reversal
# ===========================================================================
# Given items = ["apple", "banana", "cherry", "date", "elderberry"], print:
# 1) Items from index 1 to 3 (inclusive) - use slicing [1:4]
# 2) The list in reverse order

items = ["apple", "banana", "cherry", "date", "elderberry"]

# YOUR CODE HERE
print(items[1:4])
items.reverse()
print(items)

# Expected output:
# ['banana', 'cherry', 'date']
# ['elderberry', 'date', 'cherry', 'banana', 'apple']


# ===========================================================================
# Problem 4: List Comprehension - Even Numbers
# ===========================================================================
# Use list comprehension to create a list of even numbers from 1 to 20

# YOUR CODE HERE
evennumbers = [x for x in range(1,21) if x % 2 == 0]
print(evennumbers)

# Expected output:
# [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]


# ===========================================================================
# Problem 5: Combine Lists and Squares with Comprehension
# ===========================================================================
# Given two lists a = [1,2,3] and b = [4,5,6]:
# 1) Combine them into one list
# 2) Use list comprehension to create a list of their squares

a = [1, 2, 3]
b = [4, 5, 6]

# YOUR CODE HERE
combined = a+b
print(f"Combined: {combined}")
squares = [x**2 for x in combined]
print(f"Squares: {squares}")

# Expected output:
# Combined: [1, 2, 3, 4, 5, 6]
# Squares: [1, 4, 9, 16, 25, 36]


if __name__ == "__main__":
    print("Run the code above each problem to test it!")
    print("Compare your output to the '# Expected output:' comments.")
