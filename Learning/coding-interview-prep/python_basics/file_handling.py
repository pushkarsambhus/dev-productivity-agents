# File handling lets your program read from and write to files on your computer.
# The 'with' statement automatically closes the file when done — even if an error occurs.

import os

# --- Writing to a file ---
# "w" mode creates the file if it doesn't exist, or OVERWRITES it if it does
def write_file(filename, content):
    with open(filename, "w") as file:    # opens file; 'file' is our handle to it
        file.write(content)
    print(f"Written to {filename}")

# --- Appending to a file ---
# "a" mode adds to the END of the file without erasing existing content
def append_to_file(filename, content):
    with open(filename, "a") as file:
        file.write(content)
    print(f"Appended to {filename}")

# --- Reading an entire file ---
def read_file(filename):
    with open(filename, "r") as file:    # "r" = read mode
        content = file.read()            # reads the whole file as a string
    return content

# --- Reading line by line ---
def read_lines(filename):
    with open(filename, "r") as file:
        lines = file.readlines()         # returns a list where each item is one line
    return lines

if __name__ == "__main__":
    test_file = "/tmp/python_basics_test.txt"

    write_file(test_file, "Line 1: Hello from Python!\n")
    append_to_file(test_file, "Line 2: File handling is easy.\n")
    append_to_file(test_file, "Line 3: Always use 'with' to open files.\n")

    print("\n--- Full file contents ---")
    print(read_file(test_file))

    print("--- Line by line ---")
    for i, line in enumerate(read_lines(test_file), start=1):
        print(f"  Line {i}: {line.strip()}")

    # Clean up the test file
    os.remove(test_file)
    print("\nTest file removed.")
