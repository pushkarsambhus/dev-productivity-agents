# Practice: Error Handling
# In these exercises you will practice: try/except, multiple exception handlers, else, and finally

# ===========================================================================
# Problem 1: Safe Division
# ===========================================================================
# Write a safe_divide(a, b) function using try/except that:
# - Handles ZeroDivisionError and returns None on error
# - Otherwise returns the result of a / b
# Test with valid and invalid inputs.

# YOUR CODE HERE

# Expected output:
# 2.0
# None
# None


# ===========================================================================
# Problem 2: Safe Type Conversion
# ===========================================================================
# Write a safe_convert(value, type_fn) function that:
# - Tries to convert a value using the type_fn (e.g., int, float)
# - Returns None if conversion fails (e.g., int("hello"))
# Test with valid and invalid conversions.

# YOUR CODE HERE

# Expected output:
# 42
# None
# 3.14
# None


# ===========================================================================
# Problem 3: File Reading with Finally
# ===========================================================================
# Write a function that:
# - Tries to read a file (use /tmp/missing.txt which doesn't exist)
# - Catches FileNotFoundError with a helpful message
# - Uses finally to print "Attempt complete" regardless of outcome

# YOUR CODE HERE

# Expected output:
# File /tmp/missing.txt not found
# Attempt complete


# ===========================================================================
# Problem 4: Multiple Exception Types
# ===========================================================================
# Write a function that accepts a list of values and:
# - Catches IndexError if list is empty
# - Catches TypeError if values aren't numeric
# - Catches ValueError if conversion fails
# Test with various problematic inputs.

# YOUR CODE HERE

# Expected output:
# Cannot access empty list
# All values must be numeric
# Cannot convert to number


# ===========================================================================
# Problem 5: try/except/else/finally Complete Example
# ===========================================================================
# Demonstrate all four blocks:
# - try: attempt to perform a safe operation
# - except: handle exceptions
# - else: prints "Success!" ONLY if no exception
# - finally: always prints "Done."
# Test with both successful and failing cases.

# YOUR CODE HERE

# Expected output:
# Success!
# Done.
# Error occurred
# Done.


if __name__ == "__main__":
    print("Run the code above each problem to test it!")
    print("Compare your output to the '# Expected output:' comments.")
