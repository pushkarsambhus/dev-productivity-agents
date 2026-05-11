# SOLUTIONS: Loops
# These are reference solutions — there are often multiple valid ways to solve each problem!

# ===========================================================================
# Problem 1 Solution: Multiplication Table
# ===========================================================================

for i in range(1, 11):
    print(f"7 x {i} = {7 * i}")


# ===========================================================================
# Problem 2 Solution: Powers of 2
# ===========================================================================

power = 1
while power < 1000:
    print(power)
    power *= 2


# ===========================================================================
# Problem 3 Solution: Enumerate with 1-Based Indexing
# ===========================================================================

words = ["python", "java", "ruby", "go", "rust"]
for index, word in enumerate(words, start=1):
    print(f"{index}. {word}")


# ===========================================================================
# Problem 4 Solution: Find First Number Greater Than 6
# ===========================================================================

numbers = [4, 7, 2, 9, 1, 5]
for num in numbers:
    if num > 6:
        print(num)
        break


# ===========================================================================
# Problem 5 Solution: Zip Names and Scores
# ===========================================================================

names = ["Alice", "Bob", "Carol"]
scores = [95, 82, 91]
for name, score in zip(names, scores):
    print(f"{name}: {score}")


if __name__ == "__main__":
    print("=== Running all solutions ===")

    print("\nProblem 1:")
    for i in range(1, 11):
        print(f"7 x {i} = {7 * i}")

    print("\nProblem 2:")
    power = 1
    while power < 1000:
        print(power)
        power *= 2

    print("\nProblem 3:")
    words = ["python", "java", "ruby", "go", "rust"]
    for index, word in enumerate(words, start=1):
        print(f"{index}. {word}")

    print("\nProblem 4:")
    numbers = [4, 7, 2, 9, 1, 5]
    for num in numbers:
        if num > 6:
            print(num)
            break

    print("\nProblem 5:")
    names = ["Alice", "Bob", "Carol"]
    scores = [95, 82, 91]
    for name, score in zip(names, scores):
        print(f"{name}: {score}")
