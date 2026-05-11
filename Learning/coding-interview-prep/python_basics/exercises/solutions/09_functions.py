# SOLUTIONS: Functions
# These are reference solutions — there are often multiple valid ways to solve each problem!

import math

# ===========================================================================
# Problem 1 Solution: Function with Default Argument
# ===========================================================================

def greet(name, greeting="Hello"):
    print(f"{greeting}, {name}!")

greet("Alice")
greet("Alice", "Hi")


# ===========================================================================
# Problem 2 Solution: Function with **kwargs
# ===========================================================================

def calculate_area(shape, **kwargs):
    if shape == "circle":
        radius = kwargs["radius"]
        return math.pi * radius ** 2
    elif shape == "rectangle":
        width = kwargs["width"]
        height = kwargs["height"]
        return width * height

circle_area = calculate_area("circle", radius=5)
rectangle_area = calculate_area("rectangle", width=4, height=5)
print(f"Circle area: {circle_area:.1f}")
print(f"Rectangle area: {rectangle_area}")


# ===========================================================================
# Problem 3 Solution: Function with *args
# ===========================================================================

def stats(*numbers):
    return (min(numbers), max(numbers), sum(numbers) / len(numbers))

result = stats(3, 1, 4, 1, 5, 9, 2, 6)
print(result)


# ===========================================================================
# Problem 4 Solution: Check if a Word is a Palindrome
# ===========================================================================

def is_palindrome(word):
    return word == word[::-1]

print(is_palindrome("racecar"))
print(is_palindrome("hello"))


# ===========================================================================
# Problem 5 Solution: FizzBuzz Function
# ===========================================================================

def fizzbuzz(n):
    if n % 15 == 0:
        return "FizzBuzz"
    elif n % 3 == 0:
        return "Fizz"
    elif n % 5 == 0:
        return "Buzz"
    else:
        return n

for i in range(1, 21):
    print(fizzbuzz(i))


if __name__ == "__main__":
    print("=== Running all solutions ===")

    print("\nProblem 1:")
    def greet(name, greeting="Hello"):
        print(f"{greeting}, {name}!")

    greet("Alice")
    greet("Alice", "Hi")

    print("\nProblem 2:")
    def calculate_area(shape, **kwargs):
        if shape == "circle":
            radius = kwargs["radius"]
            return math.pi * radius ** 2
        elif shape == "rectangle":
            width = kwargs["width"]
            height = kwargs["height"]
            return width * height

    circle_area = calculate_area("circle", radius=5)
    rectangle_area = calculate_area("rectangle", width=4, height=5)
    print(f"Circle area: {circle_area:.1f}")
    print(f"Rectangle area: {rectangle_area}")

    print("\nProblem 3:")
    def stats(*numbers):
        return (min(numbers), max(numbers), sum(numbers) / len(numbers))

    result = stats(3, 1, 4, 1, 5, 9, 2, 6)
    print(result)

    print("\nProblem 4:")
    def is_palindrome(word):
        return word == word[::-1]

    print(is_palindrome("racecar"))
    print(is_palindrome("hello"))

    print("\nProblem 5:")
    def fizzbuzz(n):
        if n % 15 == 0:
            return "FizzBuzz"
        elif n % 3 == 0:
            return "Fizz"
        elif n % 5 == 0:
            return "Buzz"
        else:
            return n

    for i in range(1, 21):
        print(fizzbuzz(i))
