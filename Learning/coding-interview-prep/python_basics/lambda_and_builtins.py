# Lambda functions are tiny, one-line functions without a name.
# Python also has built-in tools like map, filter, sorted, zip, and enumerate
# that process collections of data efficiently.

# --- Lambda: a quick, nameless function ---
square = lambda x: x ** 2          # same as: def square(x): return x ** 2
add = lambda a, b: a + b           # takes two inputs, returns their sum

# --- map(): apply a function to every item in a list ---
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x ** 2, numbers))   # [1, 4, 9, 16, 25]

# --- filter(): keep only items where the function returns True ---
evens = list(filter(lambda x: x % 2 == 0, numbers))  # [2, 4]

# --- sorted(): return a sorted copy of a list ---
words = ["banana", "apple", "cherry", "date"]
sorted_words = sorted(words)                          # alphabetical order
sorted_by_length = sorted(words, key=lambda w: len(w))  # shortest to longest

# --- zip(): pair up two lists item by item ---
names = ["Alice", "Bob", "Carol"]
scores = [95, 82, 78]
paired = list(zip(names, scores))   # [("Alice", 95), ("Bob", 82), ("Carol", 78)]

# --- enumerate(): loop with index + value ---
enumerated = list(enumerate(words))  # [(0, "banana"), (1, "apple"), ...]

if __name__ == "__main__":
    print("Square of 7:", square(7))
    print("3 + 4 =", add(3, 4))
    print("Squared:", squared)
    print("Evens:", evens)
    print("Sorted alphabetically:", sorted_words)
    print("Sorted by length:", sorted_by_length)
    print("Paired:", paired)
    print("Enumerated:", enumerated)
