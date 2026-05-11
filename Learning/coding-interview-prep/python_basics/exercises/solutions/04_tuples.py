# SOLUTIONS: Tuples
# These are reference solutions — there are often multiple valid ways to solve each problem!

# ===========================================================================
# Problem 1 Solution: Tuple Unpacking
# ===========================================================================

point = (4, 7)
x, y = point
print(f"Point is at x={x}, y={y}")


# ===========================================================================
# Problem 2 Solution: Tuple Immutability with Exception Handling
# ===========================================================================

colors = ("red", "green", "blue")
try:
    colors[0] = "yellow"
except TypeError:
    print("Cannot modify tuple - tuples are immutable")


# ===========================================================================
# Problem 3 Solution: Unpack and Calculate Aspect Ratio
# ===========================================================================

dimensions = (1920, 1080)
width, height = dimensions
aspect_ratio = width / height
print(aspect_ratio)


# ===========================================================================
# Problem 4 Solution: Function Returning Tuple with Min, Max, Average
# ===========================================================================

def stats(numbers):
    return (min(numbers), max(numbers), sum(numbers) / len(numbers))

result = stats([3, 1, 4, 1, 5, 9, 2, 6])
min_val, max_val, avg_val = result
print(f"Min: {min_val}, Max: {max_val}, Average: {avg_val}")


# ===========================================================================
# Problem 5 Solution: Unpack Tuples in a Loop
# ===========================================================================

records = [("Alice", 95), ("Bob", 82), ("Carol", 91)]
for name, score in records:
    print(f"{name}: {score}")


if __name__ == "__main__":
    print("=== Running all solutions ===")

    print("\nProblem 1:")
    point = (4, 7)
    x, y = point
    print(f"Point is at x={x}, y={y}")

    print("\nProblem 2:")
    colors = ("red", "green", "blue")
    try:
        colors[0] = "yellow"
    except TypeError:
        print("Cannot modify tuple - tuples are immutable")

    print("\nProblem 3:")
    dimensions = (1920, 1080)
    width, height = dimensions
    aspect_ratio = width / height
    print(aspect_ratio)

    print("\nProblem 4:")
    def stats(numbers):
        return (min(numbers), max(numbers), sum(numbers) / len(numbers))

    result = stats([3, 1, 4, 1, 5, 9, 2, 6])
    min_val, max_val, avg_val = result
    print(f"Min: {min_val}, Max: {max_val}, Average: {avg_val}")

    print("\nProblem 5:")
    records = [("Alice", 95), ("Bob", 82), ("Carol", 91)]
    for name, score in records:
        print(f"{name}: {score}")
