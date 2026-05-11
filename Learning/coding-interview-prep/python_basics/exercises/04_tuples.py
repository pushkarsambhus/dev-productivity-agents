# Practice: Tuples
# In these exercises you will practice: tuple creation, unpacking, immutability, and functions returning tuples

# ===========================================================================
# Problem 1: Tuple Unpacking
# ===========================================================================
# Create a tuple point = (4, 7). Unpack it into x and y variables.
# Print in the format: "Point is at x=4, y=7"

point = (4, 7)

# YOUR CODE HERE

# Expected output:
# Point is at x=4, y=7


# ===========================================================================
# Problem 2: Tuple Immutability with Exception Handling
# ===========================================================================
# Create a tuple of 3 colors. Try to change the first color and catch the TypeError.
# Print an appropriate error message.

colors = ("red", "green", "blue")

# YOUR CODE HERE

# Expected output:
# Cannot modify tuple - tuples are immutable


# ===========================================================================
# Problem 3: Unpack and Calculate Aspect Ratio
# ===========================================================================
# Given dimensions = (1920, 1080), unpack into width and height.
# Calculate the aspect ratio (width / height) and print it as a float.

dimensions = (1920, 1080)

# YOUR CODE HERE

# Expected output:
# 1.7777777777777777


# ===========================================================================
# Problem 4: Function Returning Tuple with Min, Max, Average
# ===========================================================================
# Create a function that takes a list and returns a tuple of (minimum, maximum, average).
# Test it with the list [3, 1, 4, 1, 5, 9, 2, 6].

# YOUR CODE HERE

# Expected output:
# Min: 1, Max: 9, Average: 3.875


# ===========================================================================
# Problem 5: Unpack Tuples in a Loop
# ===========================================================================
# Given a list of tuples representing student records (name, score),
# loop through and print each name and score in the format: "Alice: 95"

records = [("Alice", 95), ("Bob", 82), ("Carol", 91)]

# YOUR CODE HERE

# Expected output:
# Alice: 95
# Bob: 82
# Carol: 91


if __name__ == "__main__":
    print("Run the code above each problem to test it!")
    print("Compare your output to the '# Expected output:' comments.")
