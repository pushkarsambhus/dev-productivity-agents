# Practice: Dictionaries
# In these exercises you will practice: dict creation, access, modification, iteration, and comprehension

# ===========================================================================
# Problem 1: Create and Iterate Through Dictionary
# ===========================================================================
# Create a dictionary for a book with keys: title, author, year, pages.
# Print each key-value pair using .items()

book = {
    "title": "1984",
    "author": "George Orwell",
    "year": 1949,
    "pages": 328
}

# YOUR CODE HERE

# Expected output:
# title: 1984
# author: George Orwell
# year: 1949
# pages: 328


# ===========================================================================
# Problem 2: Find Key with Highest Value
# ===========================================================================
# Given scores = {"Alice": 95, "Bob": 82, "Carol": 91, "Dave": 78},
# find and print the name of the student with the highest score.

scores = {"Alice": 95, "Bob": 82, "Carol": 91, "Dave": 78}

# YOUR CODE HERE

# Expected output:
# Alice has the highest score: 95


# ===========================================================================
# Problem 3: Add, Update, and Remove from Dictionary
# ===========================================================================
# Starting with scores = {"Alice": 95, "Bob": 82, "Carol": 91, "Dave": 78}:
# 1) Add a new student "Eve" with score 88
# 2) Update Bob's score to 85
# 3) Remove Dave from the dictionary
# Print the final dictionary

scores = {"Alice": 95, "Bob": 82, "Carol": 91, "Dave": 78}

# YOUR CODE HERE

# Expected output:
# {'Alice': 95, 'Bob': 85, 'Carol': 91, 'Eve': 88}


# ===========================================================================
# Problem 4: Dictionary Comprehension - Numbers to Cubes
# ===========================================================================
# Use a dictionary comprehension to create a mapping of numbers 1-5 to their cubes.
# Expected: {1: 1, 2: 8, 3: 27, 4: 64, 5: 125}

# YOUR CODE HERE

# Expected output:
# {1: 1, 2: 8, 3: 27, 4: 64, 5: 125}


# ===========================================================================
# Problem 5: Count Words by First Letter
# ===========================================================================
# Given words = ["apple", "banana", "cherry", "avocado", "blueberry"],
# use a dictionary to count how many words start with each letter.

words = ["apple", "banana", "cherry", "avocado", "blueberry"]

# YOUR CODE HERE

# Expected output:
# {'a': 2, 'b': 2, 'c': 1}


if __name__ == "__main__":
    print("Run the code above each problem to test it!")
    print("Compare your output to the '# Expected output:' comments.")
