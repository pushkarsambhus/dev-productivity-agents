# Practice: Functions
# In these exercises you will practice: function definition, parameters, default arguments, *args, **kwargs

# ===========================================================================
# Problem 1: Function with Default Argument
# ===========================================================================
# Write a function greet(name, greeting="Hello") that prints "Hello, Alice!"
# Call it with just a name and then with a custom greeting.

# YOUR CODE HERE

# Expected output (two calls):
# Hello, Alice!
# Hi, Alice!


# ===========================================================================
# Problem 2: Function with **kwargs
# ===========================================================================
# Write a function calculate_area(shape, **kwargs) that:
# - If shape="circle", use kwargs["radius"] and return area (pi * r^2)
# - If shape="rectangle", use kwargs["width"] and kwargs["height"] and return area
# Test both cases.

import math

# YOUR CODE HERE

# Expected output:
# Circle area: 78.5
# Rectangle area: 20


# ===========================================================================
# Problem 3: Function with *args
# ===========================================================================
# Write a function stats(*numbers) that returns a tuple of (min, max, average)
# for any number of input arguments.
# Test with stats(3, 1, 4, 1, 5, 9, 2, 6)

# YOUR CODE HERE

# Expected output:
# (1, 9, 4.375)


# ===========================================================================
# Problem 4: Check if a Word is a Palindrome
# ===========================================================================
# Write a function is_palindrome(word) that returns True if the word reads
# the same forwards and backwards, False otherwise.
# Test with "racecar" and "hello"

# YOUR CODE HERE

# Expected output:
# True
# False


# ===========================================================================
# Problem 5: FizzBuzz Function
# ===========================================================================
# Write a function fizzbuzz(n) that:
# - Returns "Fizz" if n divisible by 3
# - Returns "Buzz" if n divisible by 5
# - Returns "FizzBuzz" if divisible by both
# - Returns the number itself otherwise
# Test with numbers 1-20 and print results.

# YOUR CODE HERE

# Expected output:
# 1
# 2
# Fizz
# 4
# Buzz
# Fizz
# 7
# 8
# Fizz
# Buzz
# 11
# Fizz
# 13
# 14
# FizzBuzz
# 16
# 17
# Fizz
# 19
# Buzz


if __name__ == "__main__":
    print("Run the code above each problem to test it!")
    print("Compare your output to the '# Expected output:' comments.")
