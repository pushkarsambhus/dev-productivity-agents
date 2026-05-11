# List comprehensions are a concise way to build lists.
# Advanced comprehensions can use conditions and even nest inside each other.

# --- Basic comprehension (review) ---
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
squares = [x ** 2 for x in numbers]              # square every number

# --- Conditional comprehension: include only items that pass a test ---
evens = [x for x in numbers if x % 2 == 0]       # only even numbers
odd_squares = [x ** 2 for x in numbers if x % 2 != 0]  # squares of odd numbers

# --- Inline if/else inside comprehension: transform based on condition ---
labels = ["even" if x % 2 == 0 else "odd" for x in numbers]

# --- Nested comprehension: flatten a 2D list into 1D ---
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [item for row in matrix for item in row]   # reads: "for each row, for each item in row"

# --- Nested comprehension: create a multiplication table ---
times_table = [[row * col for col in range(1, 4)] for row in range(1, 4)]

# --- Dict comprehension with condition ---
word_lengths = {word: len(word) for word in ["apple", "hi", "banana", "ok"] if len(word) > 2}

# --- Set comprehension: unique remainders when dividing by 3 ---
remainders = {x % 3 for x in range(15)}

if __name__ == "__main__":
    print("Squares:", squares)
    print("Evens only:", evens)
    print("Squares of odds:", odd_squares)
    print("Labels:", labels)
    print("Flattened matrix:", flat)
    print("3x3 Times table:")
    for row in times_table:
        print(" ", row)
    print("Word lengths (>2 chars):", word_lengths)
    print("Remainders mod 3:", remainders)
