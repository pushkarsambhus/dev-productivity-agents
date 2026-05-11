# SOLUTIONS: Sets
# These are reference solutions — there are often multiple valid ways to solve each problem!

# ===========================================================================
# Problem 1 Solution: Remove Duplicates with Sets
# ===========================================================================

numbers = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
unique = set(numbers)
print(unique)


# ===========================================================================
# Problem 2 Solution: Set Operations - Union, Intersection, Difference
# ===========================================================================

a = {1, 2, 3, 4, 5}
b = {4, 5, 6, 7, 8}
print(f"Union: {a | b}")
print(f"Intersection: {a & b}")
print(f"Difference (a - b): {a - b}")
print(f"Symmetric difference: {a ^ b}")


# ===========================================================================
# Problem 3 Solution: Find Students in Both Classes
# ===========================================================================

class_a = ["Alice", "Bob", "Charlie", "Diana"]
class_b = ["Bob", "Diana", "Eve", "Frank"]
set_a = set(class_a)
set_b = set(class_b)
print(f"In both classes: {set_a & set_b}")
print(f"Only in class A: {set_a - set_b}")
print(f"In either class: {set_a | set_b}")


# ===========================================================================
# Problem 4 Solution: Subset Checking
# ===========================================================================

subset1 = {1, 2, 3}
superset = {1, 2, 3, 4, 5}
subset2 = {1, 2, 6}

print(f"{subset1} is subset of {superset}: {subset1.issubset(superset)}")
print(f"{subset2} is subset of {superset}: {subset2.issubset(superset)}")


# ===========================================================================
# Problem 5 Solution: Count Unique Characters in a String
# ===========================================================================

word = "mississippi"
unique_chars = set(word)
print(f"Unique characters: {len(unique_chars)}")
print(f"Characters: {unique_chars}")


if __name__ == "__main__":
    print("=== Running all solutions ===")

    print("\nProblem 1:")
    numbers = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
    unique = set(numbers)
    print(unique)

    print("\nProblem 2:")
    a = {1, 2, 3, 4, 5}
    b = {4, 5, 6, 7, 8}
    print(f"Union: {a | b}")
    print(f"Intersection: {a & b}")
    print(f"Difference (a - b): {a - b}")
    print(f"Symmetric difference: {a ^ b}")

    print("\nProblem 3:")
    class_a = ["Alice", "Bob", "Charlie", "Diana"]
    class_b = ["Bob", "Diana", "Eve", "Frank"]
    set_a = set(class_a)
    set_b = set(class_b)
    print(f"In both classes: {set_a & set_b}")
    print(f"Only in class A: {set_a - set_b}")
    print(f"In either class: {set_a | set_b}")

    print("\nProblem 4:")
    subset1 = {1, 2, 3}
    superset = {1, 2, 3, 4, 5}
    subset2 = {1, 2, 6}
    print(f"{subset1} is subset of {superset}: {subset1.issubset(superset)}")
    print(f"{subset2} is subset of {superset}: {subset2.issubset(superset)}")

    print("\nProblem 5:")
    word = "mississippi"
    unique_chars = set(word)
    print(f"Unique characters: {len(unique_chars)}")
    print(f"Characters: {unique_chars}")
