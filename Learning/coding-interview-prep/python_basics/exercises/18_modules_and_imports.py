# Practice: Modules and Standard Library
# In these exercises you will practice: importing modules and using common standard library functions

# ===========================================================================
# Problem 1: Math Module
# ===========================================================================
# Use the math module to:
# 1) Calculate hypotenuse of a 3-4-5 triangle using math.sqrt()
# 2) Get floor of 7.3
# 3) Get ceiling of 7.3
# 4) Calculate log base 2 of 64

import math

# YOUR CODE HERE

# Expected output:
# Hypotenuse: 5.0
# Floor: 7
# Ceiling: 8
# Log base 2: 6.0


# ===========================================================================
# Problem 2: Random Module - Dice Rolling
# ===========================================================================
# Use random.randint() to simulate rolling two dice 10 times.
# Print each roll and count how many times the sum equals 7.

import random

# YOUR CODE HERE

# Expected output:
# (Sample output - will vary due to randomness)
# Roll 1: (3, 4) = 7
# Roll 2: (2, 5) = 7
# ...
# Total 7s: X


# ===========================================================================
# Problem 3: Datetime Module
# ===========================================================================
# Use datetime to:
# 1) Get today's date
# 2) Calculate days until New Year's Day next year
# 3) Calculate your age in days (assume born Jan 1, 2000)

from datetime import datetime, timedelta

# YOUR CODE HERE

# Expected output:
# Today: 2026-03-25
# Days until New Year: X
# Days since Jan 1, 2000: X


# ===========================================================================
# Problem 4: OS Module
# ===========================================================================
# Use os and os.path to:
# 1) Get the current working directory
# 2) Check if /tmp exists
# 3) List the first 5 items in /tmp

import os

# YOUR CODE HERE

# Expected output:
# Current directory: /path/to/current
# /tmp exists: True
# First 5 items in /tmp:
# item1
# item2
# ...


# ===========================================================================
# Problem 5: Collections.Counter
# ===========================================================================
# Use collections.Counter to count word frequency in:
# "to be or not to be that is the question"
# Print the 5 most common words.

from collections import Counter

# YOUR CODE HERE

# Expected output:
# be: 2
# to: 2
# or: 1
# not: 1
# that: 1


if __name__ == "__main__":
    print("Run the code above each problem to test it!")
    print("Compare your output to the '# Expected output:' comments.")
