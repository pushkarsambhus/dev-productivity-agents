# Practice: Decorators
# In these exercises you will practice: creating decorators, decorator factories, and property decorators

# ===========================================================================
# Problem 1: Timer Decorator
# ===========================================================================
# Write a @timer decorator that measures and prints how long a function takes.
# Test it on a function that loops 1 million times.
# Expected output format: "Function 'function_name' took 0.123 seconds"

import time

# YOUR CODE HERE

# Expected output:
# Function 'slow_function' took approximately 0.1 seconds


# ===========================================================================
# Problem 2: Logger Decorator
# ===========================================================================
# Write a @logger decorator that prints:
# - "Calling: function_name" before execution
# - "Done: function_name" after execution
# Test with a simple function.

# YOUR CODE HERE

# Expected output:
# Calling: greet
# Hello, Alice!
# Done: greet


# ===========================================================================
# Problem 3: Retry Decorator Factory
# ===========================================================================
# Write a @retry(times=3) decorator factory that retries a function up to N times
# if it raises an exception.
# Test with a function that sometimes fails.

# YOUR CODE HERE

# Expected output:
# Attempt 1 failed
# Attempt 2 failed
# Attempt 3 succeeded!


# ===========================================================================
# Problem 4: Circle Class with Property Decorators
# ===========================================================================
# Create a Circle class with _radius private attribute.
# Use @property for getter, setter (reject negative), and auto-compute:
# - area property (computed from radius)
# - circumference property (computed from radius)

import math

# YOUR CODE HERE

# Expected output:
# Radius: 5
# Area: 78.5
# Circumference: 31.4
# Radius cannot be negative


# ===========================================================================
# Problem 5: Validate Arguments Decorator
# ===========================================================================
# Write a @validate_positive decorator that raises ValueError if any numeric
# argument is negative.
# Test with an add(a, b) function.

# YOUR CODE HERE

# Expected output:
# 8
# Argument values cannot be negative
# Argument values cannot be negative


if __name__ == "__main__":
    print("Run the code above each problem to test it!")
    print("Compare your output to the '# Expected output:' comments.")
