# SOLUTIONS: Lists
# These are reference solutions — there are often multiple valid ways to solve each problem!

# ===========================================================================
# Problem 1 Solution: Add and Insert List Elements
# ===========================================================================

fruits = ["apple", "banana", "cherry", "date", "elderberry"]
fruits.append("mango")
fruits.insert(2, "kiwi")
print(fruits)


# ===========================================================================
# Problem 2 Solution: List Functions - Sort, Max, Min, Sum
# ===========================================================================

numbers = [5, 2, 8, 1, 9, 3, 7, 4, 6]
print(f"Sorted: {sorted(numbers)}")
print(f"Max: {max(numbers)}")
print(f"Min: {min(numbers)}")
print(f"Sum: {sum(numbers)}")


# ===========================================================================
# Problem 3 Solution: List Slicing and Reversal
# ===========================================================================

items = ["apple", "banana", "cherry", "date", "elderberry"]
print(items[1:4])
print(items[::-1])


# ===========================================================================
# Problem 4 Solution: List Comprehension - Even Numbers
# ===========================================================================

even_numbers = [x for x in range(1, 21) if x % 2 == 0]
print(even_numbers)


# ===========================================================================
# Problem 5 Solution: Combine Lists and Squares with Comprehension
# ===========================================================================

a = [1, 2, 3]
b = [4, 5, 6]
combined = a + b
squares = [x ** 2 for x in combined]
print(f"Combined: {combined}")
print(f"Squares: {squares}")


if __name__ == "__main__":
    print("=== Running all solutions ===")

    print("\nProblem 1:")
    fruits = ["apple", "banana", "cherry", "date", "elderberry"]
    fruits.append("mango")
    fruits.insert(2, "kiwi")
    print(fruits)

    print("\nProblem 2:")
    numbers = [5, 2, 8, 1, 9, 3, 7, 4, 6]
    print(f"Sorted: {sorted(numbers)}")
    print(f"Max: {max(numbers)}")
    print(f"Min: {min(numbers)}")
    print(f"Sum: {sum(numbers)}")

    print("\nProblem 3:")
    items = ["apple", "banana", "cherry", "date", "elderberry"]
    print(items[1:4])
    print(items[::-1])

    print("\nProblem 4:")
    even_numbers = [x for x in range(1, 21) if x % 2 == 0]
    print(even_numbers)

    print("\nProblem 5:")
    a = [1, 2, 3]
    b = [4, 5, 6]
    combined = a + b
    squares = [x ** 2 for x in combined]
    print(f"Combined: {combined}")
    print(f"Squares: {squares}")
