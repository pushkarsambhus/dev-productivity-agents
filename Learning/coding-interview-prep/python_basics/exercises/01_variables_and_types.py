# Practice: Variables and Data Types
# In these exercises you will practice: creating variables, understanding data types, type conversion, and printing with types

# ===========================================================================
# Problem 1: Create and Print Variables with Types
# ===========================================================================
# Create the following variables and print each one with its type using type()

name = "Jordan"
age = 28
height = 5.9
is_employed = True

# YOUR CODE HERE
print(name , type(name))
print(age, type(age))
print(height, type(height))
print(is_employed, type(is_employed))
# Expected output:
# Jordan <class 'str'>
# 28 <class 'int'>
# 5.9 <class 'float'>
# True <class 'bool'>


# ===========================================================================
# Problem 2: String to Integer Conversion
# ===========================================================================
# Convert the string "42" to an integer, multiply it by 3, and print the result

number_string = "42"

# YOUR CODE HERE
print(int(number_string) * 3)

# Expected output:
# 126


# ===========================================================================
# Problem 3: Float to Int Conversion and Difference
# ===========================================================================
# Convert the float 3.7 to an integer (truncates to 3), then print both the original float,
# the converted int, and the difference between them

original_float = 3.7

# YOUR CODE HERE
print(f"Original: {original_float}")
print(f"Converted: {int(original_float)}")
print(f"Difference: {round(original_float - int(original_float),1)}")

# Expected output:
# Original: 3.7
# Converted: 3
# Difference: 0.7


# ===========================================================================
# Problem 4: Rounding a Float
# ===========================================================================
# Create a variable pi = 3.14159 and print it rounded to 2 decimal places using round()

pi = 3.14159

# YOUR CODE HERE
print(round(pi,2))

# Expected output:
# 3.14


# ===========================================================================
# Problem 5: Calculate Total Cost
# ===========================================================================
# Given price = 19.99 and quantity = 4, calculate the total cost and print
# it in the format: "Total: $79.96"

price = 19.99
quantity = 4

# YOUR CODE HERE
print(f"Total: ${price * quantity}")
# Expected output:
# Total: $79.96


if __name__ == "__main__":
    print("Run the code above each problem to test it!")
    print("Compare your output to the '# Expected output:' comments.")
