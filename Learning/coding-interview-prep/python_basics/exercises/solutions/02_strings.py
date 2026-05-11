# SOLUTIONS: String Operations
# These are reference solutions — there are often multiple valid ways to solve each problem!

# ===========================================================================
# Problem 1 Solution: String Case Conversion and Word Count
# ===========================================================================

sentence = "the quick brown fox"
print(sentence.title())
print(sentence.upper())
print(len(sentence.split()))


# ===========================================================================
# Problem 2 Solution: Strip and Replace
# ===========================================================================

greeting = "  Hello, World!  "
greeting = greeting.strip()
greeting = greeting.replace("World", "Jordan")
print(greeting)


# ===========================================================================
# Problem 3 Solution: Extract First and Last Name
# ===========================================================================

full_name = "Ada Lovelace"
names = full_name.split()
first_name = names[0]
last_name = names[1]
print(f"First name: {first_name}")
print(f"Last name: {last_name}")


# ===========================================================================
# Problem 4 Solution: Check if a String is a Palindrome
# ===========================================================================

s = "racecar"
is_palindrome = s == s[::-1]
print(is_palindrome)


# ===========================================================================
# Problem 5 Solution: F-String Formatting
# ===========================================================================

name = "Alice"
score = 95.5
print(f"{name} scored {score} points (grade: A)")


if __name__ == "__main__":
    print("=== Running all solutions ===")

    print("\nProblem 1:")
    sentence = "the quick brown fox"
    print(sentence.title())
    print(sentence.upper())
    print(len(sentence.split()))

    print("\nProblem 2:")
    greeting = "  Hello, World!  "
    greeting = greeting.strip()
    greeting = greeting.replace("World", "Jordan")
    print(greeting)

    print("\nProblem 3:")
    full_name = "Ada Lovelace"
    names = full_name.split()
    first_name = names[0]
    last_name = names[1]
    print(f"First name: {first_name}")
    print(f"Last name: {last_name}")

    print("\nProblem 4:")
    s = "racecar"
    is_palindrome = s == s[::-1]
    print(is_palindrome)

    print("\nProblem 5:")
    name = "Alice"
    score = 95.5
    print(f"{name} scored {score} points (grade: A)")
