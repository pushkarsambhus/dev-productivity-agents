# SOLUTIONS: Dictionaries
# These are reference solutions — there are often multiple valid ways to solve each problem!

# ===========================================================================
# Problem 1 Solution: Create and Iterate Through Dictionary
# ===========================================================================

book = {
    "title": "1984",
    "author": "George Orwell",
    "year": 1949,
    "pages": 328
}

for key, value in book.items():
    print(f"{key}: {value}")


# ===========================================================================
# Problem 2 Solution: Find Key with Highest Value
# ===========================================================================

scores = {"Alice": 95, "Bob": 82, "Carol": 91, "Dave": 78}
highest_name = max(scores, key=scores.get)
highest_score = scores[highest_name]
print(f"{highest_name} has the highest score: {highest_score}")


# ===========================================================================
# Problem 3 Solution: Add, Update, and Remove from Dictionary
# ===========================================================================

scores = {"Alice": 95, "Bob": 82, "Carol": 91, "Dave": 78}
scores["Eve"] = 88
scores["Bob"] = 85
del scores["Dave"]
print(scores)


# ===========================================================================
# Problem 4 Solution: Dictionary Comprehension - Numbers to Cubes
# ===========================================================================

cubes = {x: x ** 3 for x in range(1, 6)}
print(cubes)


# ===========================================================================
# Problem 5 Solution: Count Words by First Letter
# ===========================================================================

words = ["apple", "banana", "cherry", "avocado", "blueberry"]
letter_count = {}
for word in words:
    first_letter = word[0]
    if first_letter in letter_count:
        letter_count[first_letter] += 1
    else:
        letter_count[first_letter] = 1
print(letter_count)


if __name__ == "__main__":
    print("=== Running all solutions ===")

    print("\nProblem 1:")
    book = {
        "title": "1984",
        "author": "George Orwell",
        "year": 1949,
        "pages": 328
    }
    for key, value in book.items():
        print(f"{key}: {value}")

    print("\nProblem 2:")
    scores = {"Alice": 95, "Bob": 82, "Carol": 91, "Dave": 78}
    highest_name = max(scores, key=scores.get)
    highest_score = scores[highest_name]
    print(f"{highest_name} has the highest score: {highest_score}")

    print("\nProblem 3:")
    scores = {"Alice": 95, "Bob": 82, "Carol": 91, "Dave": 78}
    scores["Eve"] = 88
    scores["Bob"] = 85
    del scores["Dave"]
    print(scores)

    print("\nProblem 4:")
    cubes = {x: x ** 3 for x in range(1, 6)}
    print(cubes)

    print("\nProblem 5:")
    words = ["apple", "banana", "cherry", "avocado", "blueberry"]
    letter_count = {}
    for word in words:
        first_letter = word[0]
        if first_letter in letter_count:
            letter_count[first_letter] += 1
        else:
            letter_count[first_letter] = 1
    print(letter_count)
