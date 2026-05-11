# Practice: Custom Exceptions
# In these exercises you will practice: creating custom exceptions, raising exceptions, and exception hierarchies

# ===========================================================================
# Problem 1: ValidationError Exception
# ===========================================================================
# Create a ValidationError exception class.
# Write a validate_age(age) function that raises ValidationError if age < 0 or > 150.
# Test with valid and invalid ages.

# YOUR CODE HERE

# Expected output:
# Age is valid
# Age cannot be negative
# Age cannot be greater than 150


# ===========================================================================
# Problem 2: Multiple Custom Exceptions
# ===========================================================================
# Create InsufficientFundsError and NegativeAmountError exceptions.
# Write a withdraw(balance, amount) function that:
# - Raises NegativeAmountError if amount < 0
# - Raises InsufficientFundsError if amount > balance
# - Returns new balance otherwise
# Test all cases.

# YOUR CODE HERE

# Expected output:
# Amount cannot be negative
# Insufficient funds
# New balance: 50


# ===========================================================================
# Problem 3: FileReadError Exception
# ===========================================================================
# Create a FileReadError exception.
# Write a function that tries to open a file and raises FileReadError with
# a helpful message if the file doesn't exist.
# Test with a non-existent file.

# YOUR CODE HERE

# Expected output:
# File not found: nonexistent.txt


# ===========================================================================
# Problem 4: try/except/else/finally
# ===========================================================================
# Call validate_age() with -1, 200, and 25.
# Use try/except/else/finally to handle each case.
# - except: different messages for ValueError vs other exceptions
# - else: print "Success!" only when no exception
# - finally: always print "Validation attempt complete"

# YOUR CODE HERE

# Expected output:
# Age cannot be negative
# Validation attempt complete
# Age cannot be greater than 150
# Validation attempt complete
# Success!
# Validation attempt complete


# ===========================================================================
# Problem 5: Exception Hierarchy
# ===========================================================================
# Create an exception hierarchy:
# - AppError (base)
# - DatabaseError (inherits from AppError)
# - ConnectionError (inherits from DatabaseError)
# Raise ConnectionError and catch it at each level to show the hierarchy.

# YOUR CODE HERE

# Expected output:
# Caught ConnectionError
# Caught DatabaseError
# Caught AppError


if __name__ == "__main__":
    print("Run the code above each problem to test it!")
    print("Compare your output to the '# Expected output:' comments.")
