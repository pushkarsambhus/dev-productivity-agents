# Practice: String Operations
# In these exercises you will practice: string methods, slicing, formatting, and string manipulation

# ===========================================================================
# Problem 1: String Case Conversion and Word Count
# ===========================================================================
# Given sentence = "the quick brown fox", print it in:
# 1) Title case
# 2) Uppercase
# 3) Count of words

sentence = "the quick brown fox"

# YOUR CODE HERE
print(sentence.title())
print(sentence.upper())
print(len(sentence.split()))

# Expected output:
# The Quick Brown Fox
# THE QUICK BROWN FOX
# 4


# ===========================================================================
# Problem 2: Strip and Replace
# ===========================================================================
# Given greeting = "  Hello, World!  " (note the extra spaces):
# 1) Strip the whitespace
# 2) Replace "World" with your name
# 3) Print the result

greeting = "  Hello, World!  "

# YOUR CODE HERE
print(greeting.strip().replace("World", "Pushkar"))

# Expected output:
# Hello, Jordan!
# (or with whatever name you choose)


# ===========================================================================
# Problem 3: Extract First and Last Name
# ===========================================================================
# Given full_name = "Ada Lovelace", extract and print:
# 1) The first name using split()
# 2) The last name using split()
# Use either split() or slicing

full_name = "Ada Lovelace"

# YOUR CODE HERE
items = full_name.split()
print(f"First name: {items[0]}")
print(f"Last name: {items[1]}")

# Expected output:
# First name: Ada
# Last name: Lovelace


# ===========================================================================
# Problem 4: Check if a String is a Palindrome
# ===========================================================================
# Given s = "racecar", check if it reads the same forwards and backwards
# Print True if it is a palindrome, False otherwise

s = "racecar"

# YOUR CODE HERE
print(s[::-1] == s)

# Expected output:
# True


# ===========================================================================
# Problem 5: F-String Formatting
# ===========================================================================
# Given name = "Alice" and score = 95.5, use an f-string to print:
# "Alice scored 95.5 points (grade: A)"

name = "Alice"
score = 95.5

# YOUR CODE HERE
print(f"{name} scored {score} points (grade: A)")

# Expected output:
# Alice scored 95.5 points (grade: A)


if __name__ == "__main__":
    print("Run the code above each problem to test it!")
    print("Compare your output to the '# Expected output:' comments.")
