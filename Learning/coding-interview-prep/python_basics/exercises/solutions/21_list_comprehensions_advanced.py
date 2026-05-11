# SOLUTIONS: Advanced List and Dict Comprehensions
# These are reference solutions — there are often multiple valid ways to solve each problem!

# ===========================================================================
# Problem 1 Solution: Filter Words by Length
# ===========================================================================

sentence = "the quick brown fox jumps over the lazy dog"
words = sentence.split()
long_words = [word for word in words if len(word) > 4]
print(long_words)


# ===========================================================================
# Problem 2 Solution: Flatten Nested List
# ===========================================================================

nested = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened = [num for row in nested for num in row]
print(flattened)


# ===========================================================================
# Problem 3 Solution: Conditional Labels
# ===========================================================================

labels = ["even" if x % 2 == 0 else "odd" for x in range(1, 11)]
print(labels)


# ===========================================================================
# Problem 4 Solution: Create Multiplication Table
# ===========================================================================

multiplication_table = [[i * j for j in range(1, 6)] for i in range(1, 6)]
for row in multiplication_table:
    print(row)


# ===========================================================================
# Problem 5 Solution: Invert Dictionary
# ===========================================================================

original_dict = {"a": 1, "b": 2, "c": 3}
inverted_dict = {v: k for k, v in original_dict.items()}
print(inverted_dict)


if __name__ == "__main__":
    print("=== Running all solutions ===")

    print("\nProblem 1:")
    sentence = "the quick brown fox jumps over the lazy dog"
    words = sentence.split()
    long_words = [word for word in words if len(word) > 4]
    print(long_words)

    print("\nProblem 2:")
    nested = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    flattened = [num for row in nested for num in row]
    print(flattened)

    print("\nProblem 3:")
    labels = ["even" if x % 2 == 0 else "odd" for x in range(1, 11)]
    print(labels)

    print("\nProblem 4:")
    multiplication_table = [[i * j for j in range(1, 6)] for i in range(1, 6)]
    for row in multiplication_table:
        print(row)

    print("\nProblem 5:")
    original_dict = {"a": 1, "b": 2, "c": 3}
    inverted_dict = {v: k for k, v in original_dict.items()}
    print(inverted_dict)
