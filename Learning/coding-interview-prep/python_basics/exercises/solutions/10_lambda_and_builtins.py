# SOLUTIONS: Lambda Functions and Built-in Functions
# These are reference solutions — there are often multiple valid ways to solve each problem!

# ===========================================================================
# Problem 1 Solution: Lambda to Double a Number
# ===========================================================================

double = lambda x: x * 2
print(double(7))


# ===========================================================================
# Problem 2 Solution: Map with Lambda - Squares
# ===========================================================================

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
squares = list(map(lambda x: x ** 2, numbers))
print(squares)


# ===========================================================================
# Problem 3 Solution: Filter with Lambda - Divisible by 3
# ===========================================================================

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
divisible_by_3 = list(filter(lambda x: x % 3 == 0, numbers))
print(divisible_by_3)


# ===========================================================================
# Problem 4 Solution: Sort by String Length
# ===========================================================================

words = ["banana", "apple", "cherry", "date"]
sorted_words = sorted(words, key=lambda w: len(w))
print(sorted_words)


# ===========================================================================
# Problem 5 Solution: Zip and Sort by Age
# ===========================================================================

names = ["Alice", "Bob", "Carol"]
ages = [30, 25, 35]
paired = zip(names, ages)
sorted_pairs = sorted(paired, key=lambda pair: pair[1])
for name, age in sorted_pairs:
    print(f"{name}: {age}")


if __name__ == "__main__":
    print("=== Running all solutions ===")

    print("\nProblem 1:")
    double = lambda x: x * 2
    print(double(7))

    print("\nProblem 2:")
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    squares = list(map(lambda x: x ** 2, numbers))
    print(squares)

    print("\nProblem 3:")
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    divisible_by_3 = list(filter(lambda x: x % 3 == 0, numbers))
    print(divisible_by_3)

    print("\nProblem 4:")
    words = ["banana", "apple", "cherry", "date"]
    sorted_words = sorted(words, key=lambda w: len(w))
    print(sorted_words)

    print("\nProblem 5:")
    names = ["Alice", "Bob", "Carol"]
    ages = [30, 25, 35]
    paired = zip(names, ages)
    sorted_pairs = sorted(paired, key=lambda pair: pair[1])
    for name, age in sorted_pairs:
        print(f"{name}: {age}")
