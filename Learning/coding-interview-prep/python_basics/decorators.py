# A decorator is a function that wraps another function to add extra behavior.
# Think of it like a gift wrapper — the gift (function) stays the same inside,
# but the wrapper adds something extra (like logging or timing).

import time
import functools

# --- Simple decorator: adds a message before and after a function runs ---
def announce(func):
    @functools.wraps(func)    # preserves the original function's name and docstring
    def wrapper(*args, **kwargs):
        print(f"Starting: {func.__name__}")   # runs BEFORE the function
        result = func(*args, **kwargs)         # runs the actual function
        print(f"Done: {func.__name__}")        # runs AFTER the function
        return result
    return wrapper

# --- Timing decorator: measures how long a function takes ---
def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper

# Apply decorators using the @ symbol
@announce
def say_hello(name):
    print(f"Hello, {name}!")

@timer
def slow_function():
    time.sleep(0.1)    # simulate a slow operation
    return "done"

# --- @property decorator: makes a method behave like an attribute ---
class Circle:
    def __init__(self, radius):
        self.radius = radius

    @property
    def area(self):
        # Accessed like circle.area — no parentheses needed!
        return 3.14159 * self.radius ** 2

if __name__ == "__main__":
    say_hello("Alice")
    print()

    result = slow_function()
    print("Result:", result)
    print()

    c = Circle(5)
    print(f"Circle radius: {c.radius}")
    print(f"Circle area: {c.area:.2f}")   # no () needed because of @property
