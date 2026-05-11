# Practice: File Handling
# In these exercises you will practice: reading/writing files, appending, word counting, searching, and parsing

# ===========================================================================
# Problem 1: Write and Read a File
# ===========================================================================
# Write a function that:
# 1) Creates a file "notes.txt" in /tmp/ with 3 lines of text
# 2) Reads it back and prints each line
# Use with open()...as pattern for safe file handling.

# YOUR CODE HERE

# Expected output:
# Line 1: This is the first note.
# Line 2: This is the second note.
# Line 3: This is the third note.


# ===========================================================================
# Problem 2: Append to a Log File
# ===========================================================================
# Write a function that appends a timestamped message to a log file in /tmp/.
# Call it 3 times with different messages.
# Print the entire log file contents.

# YOUR CODE HERE

# Expected output:
# [timestamp] Message 1
# [timestamp] Message 2
# [timestamp] Message 3


# ===========================================================================
# Problem 3: Count Words in a File
# ===========================================================================
# Write a function count_words(filename) that counts total words in a text file.
# Create a test file with some content and count its words.

# YOUR CODE HERE

# Expected output:
# Total words: 15


# ===========================================================================
# Problem 4: Search Lines Containing a Keyword
# ===========================================================================
# Write a function search_in_file(filename, keyword) that:
# Prints all lines containing the keyword (case-insensitive).
# Create a test file and search for a word.

# YOUR CODE HERE

# Expected output:
# python
# Python is great
# I love Python


# ===========================================================================
# Problem 5: Read and Display CSV Data as Table
# ===========================================================================
# Write a function that reads a CSV-style file (comma-separated) and
# prints each row as a formatted table.
# First, create the CSV file with sample data (name, age, city).
# Then read and display it formatted.

# YOUR CODE HERE

# Expected output:
# Name      Age  City
# Alice     25   New York
# Bob       30   Los Angeles
# Carol     28   Chicago


if __name__ == "__main__":
    print("Run the code above each problem to test it!")
    print("Compare your output to the '# Expected output:' comments.")
