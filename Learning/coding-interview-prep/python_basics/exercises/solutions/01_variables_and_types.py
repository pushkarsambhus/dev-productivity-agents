# SOLUTIONS: Variables and Data Types
# These are reference solutions — there are often multiple valid ways to solve each problem!

# ===========================================================================
# Problem 1 Solution: Create and Print Variables with Types
# ===========================================================================

name = "Jordan"
age = 28
height = 5.9
is_employed = True

print(name, type(name))
print(age, type(age))
print(height, type(height))
print(is_employed, type(is_employed))


# ===========================================================================
# Problem 2 Solution: String to Integer Conversion
# ===========================================================================

number_string = "42"
converted = int(number_string)
result = converted * 3
print(result)


# ===========================================================================
# Problem 3 Solution: Float to Int Conversion and Difference
# ===========================================================================

original_float = 3.7
converted_int = int(original_float)
difference = original_float - converted_int

print(f"Original: {original_float}")
print(f"Converted: {converted_int}")
print(f"Difference: {difference}")


# ===========================================================================
# Problem 4 Solution: Rounding a Float
# ===========================================================================

pi = 3.14159
rounded_pi = round(pi, 2)
print(rounded_pi)


# ===========================================================================
# Problem 5 Solution: Calculate Total Cost
# ===========================================================================

price = 19.99
quantity = 4
total = price * quantity
print(f"Total: ${total:.2f}")


if __name__ == "__main__":
    print("=== Running all solutions ===")
    print("\nProblem 1:")
    print(name, type(name))
    print(age, type(age))
    print(height, type(height))
    print(is_employed, type(is_employed))

    print("\nProblem 2:")
    number_string = "42"
    converted = int(number_string)
    result = converted * 3
    print(result)

    print("\nProblem 3:")
    original_float = 3.7
    converted_int = int(original_float)
    difference = original_float - converted_int
    print(f"Original: {original_float}")
    print(f"Converted: {converted_int}")
    print(f"Difference: {difference}")

    print("\nProblem 4:")
    pi = 3.14159
    rounded_pi = round(pi, 2)
    print(rounded_pi)

    print("\nProblem 5:")
    price = 19.99
    quantity = 4
    total = price * quantity
    print(f"Total: ${total:.2f}")
