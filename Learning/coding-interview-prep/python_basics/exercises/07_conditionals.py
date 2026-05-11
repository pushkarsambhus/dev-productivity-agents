# Practice: Conditional Statements
# In these exercises you will practice: if/elif/else, boolean logic, and ternary expressions

# ===========================================================================
# Problem 1: Age Categories
# ===========================================================================
# Given age = 17, print:
# - "Can vote" if age >= 18
# - "Can drive" if age >= 16
# - "Minor" if age < 16

age = 17

# YOUR CODE HERE

# Expected output:
# Can drive


# ===========================================================================
# Problem 2: Letter Grade from Score
# ===========================================================================
# Given score = 73, print the letter grade:
# - A: 90+
# - B: 80+
# - C: 70+
# - D: 60+
# - F: below 60

score = 73

# YOUR CODE HERE

# Expected output:
# C


# ===========================================================================
# Problem 3: Weather Recommendation
# ===========================================================================
# Given temperature = 28 and is_raining = False,
# print a weather recommendation using combined conditions:
# - "Stay indoors" if is_raining and temperature < 10
# - "Bring an umbrella" if is_raining and temperature >= 10
# - "Go outside!" if not is_raining and temperature > 20
# - "Wear a jacket" if not is_raining and temperature <= 20

temperature = 28
is_raining = False

# YOUR CODE HERE

# Expected output:
# Go outside!


# ===========================================================================
# Problem 4: Ternary Expression - Pass or Fail
# ===========================================================================
# Rewrite the grading logic using a ternary expression to assign "pass" (60+) or "fail" (below 60).
# Print with an f-string. Use score = 73.

score = 73

# YOUR CODE HERE

# Expected output:
# Score: 73 - Result: pass


# ===========================================================================
# Problem 5: Authentication Logic
# ===========================================================================
# Given username = "admin" and password = "secret123",
# print:
# - "Access granted" if both are correct
# - "Wrong password" if username is "admin" but password is wrong
# - "Unknown user" otherwise

username = "admin"
password = "secret123"
correct_username = "admin"
correct_password = "secret123"

# YOUR CODE HERE

# Expected output:
# Access granted


if __name__ == "__main__":
    print("Run the code above each problem to test it!")
    print("Compare your output to the '# Expected output:' comments.")
