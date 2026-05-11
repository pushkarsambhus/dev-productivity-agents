# A generator is a special function that produces values one at a time, on demand.
# Instead of creating a whole list at once, it "yields" items as you need them.
# This saves memory — perfect for large sequences!

# --- Basic generator using yield ---
def count_up(start, end):
    current = start
    while current <= end:
        yield current      # pauses here and sends the value; resumes on next call
        current += 1

# --- Generator for infinite sequences (safe because of lazy evaluation) ---
def even_numbers():
    num = 0
    while True:           # infinite loop — but we only pull values as needed
        yield num
        num += 2

# --- Generator expression: like a list comprehension, but lazy ---
# List:      [x ** 2 for x in range(10)]  — creates ALL values immediately
# Generator: (x ** 2 for x in range(10))  — creates values one at a time

def fibonacci():
    """Yields Fibonacci numbers forever."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b   # shift: new a = old b, new b = old a+b

if __name__ == "__main__":
    print("--- count_up generator ---")
    for num in count_up(1, 5):
        print(num, end=" ")
    print()

    print("\n--- First 5 even numbers ---")
    even_gen = even_numbers()
    for _ in range(5):
        print(next(even_gen), end=" ")   # next() pulls the next value
    print()

    print("\n--- Generator expression (squares) ---")
    squares_gen = (x ** 2 for x in range(1, 6))
    print(list(squares_gen))   # convert to list to see all at once

    print("\n--- First 8 Fibonacci numbers ---")
    fib = fibonacci()
    fibs = [next(fib) for _ in range(8)]
    print(fibs)
