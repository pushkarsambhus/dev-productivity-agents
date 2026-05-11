# Functions are reusable blocks of code that do a specific task.
# Instead of writing the same code repeatedly, you write it once and "call" it by name.

# --- Basic function: takes no input, returns nothing ---
def say_hello():
    print("Hello, world!")

# --- Function with parameters (inputs) ---
def greet(name):
    print(f"Hello, {name}!")

# --- Function with a default parameter (used if caller doesn't provide one) ---
def greet_with_title(name, title="Friend"):
    print(f"Hello, {title} {name}!")

# --- Function that returns a value ---
def add(a, b):
    return a + b     # sends the result back to whoever called this function

# --- Function with multiple return values ---
def min_max(numbers):
    return min(numbers), max(numbers)   # returns two values as a tuple

# --- *args: accept any number of positional arguments ---
def total(*args):
    return sum(args)   # args becomes a tuple of all passed-in values

# --- **kwargs: accept any number of keyword arguments ---
def describe(**kwargs):
    for key, value in kwargs.items():
        print(f"  {key} = {value}")

if __name__ == "__main__":
    say_hello()
    greet("Alice")
    greet_with_title("Smith", "Dr.")
    greet_with_title("Jones")          # uses default title "Friend"

    result = add(10, 25)
    print("10 + 25 =", result)

    smallest, largest = min_max([4, 1, 9, 2, 7])
    print("Min:", smallest, "| Max:", largest)

    print("Total:", total(1, 2, 3, 4, 5))

    print("Description:")
    describe(color="blue", size="large", shape="circle")
