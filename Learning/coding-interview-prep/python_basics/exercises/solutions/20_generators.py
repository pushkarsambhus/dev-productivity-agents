# SOLUTIONS: Generators
# These are reference solutions — there are often multiple valid ways to solve each problem!

# ===========================================================================
# Problem 1 Solution: Countdown Generator
# ===========================================================================

def countdown(n):
    while n >= 0:
        yield n
        n -= 1

for value in countdown(5):
    print(value)


# ===========================================================================
# Problem 2 Solution: Fibonacci Generator
# ===========================================================================

def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

fib = fibonacci()
for _ in range(10):
    print(next(fib))


# ===========================================================================
# Problem 3 Solution: Read Large File Line by Line
# ===========================================================================

def read_large_file(filepath):
    with open(filepath) as file:
        for line in file:
            yield line.rstrip('\n')

# Create test file
with open("/tmp/large_file.txt", "w") as f:
    f.write("Line 1\n")
    f.write("Line 2\n")
    f.write("Line 3\n")

# Read using generator
for line in read_large_file("/tmp/large_file.txt"):
    print(line)


# ===========================================================================
# Problem 4 Solution: Generator Expression - Even Squares
# ===========================================================================

even_squares = (x ** 2 for x in range(2, 21, 2))
result = list(even_squares)
print(result)


# ===========================================================================
# Problem 5 Solution: Batch Generator
# ===========================================================================

def batch(iterable, size):
    batch_list = []
    for item in iterable:
        batch_list.append(item)
        if len(batch_list) == size:
            yield batch_list
            batch_list = []
    if batch_list:
        yield batch_list

for b in batch(range(1, 11), 3):
    print(b)


if __name__ == "__main__":
    print("=== Running all solutions ===")

    print("\nProblem 1:")
    def countdown(n):
        while n >= 0:
            yield n
            n -= 1

    for value in countdown(5):
        print(value)

    print("\nProblem 2:")
    def fibonacci():
        a, b = 0, 1
        while True:
            yield a
            a, b = b, a + b

    fib = fibonacci()
    for _ in range(10):
        print(next(fib))

    print("\nProblem 3:")
    def read_large_file(filepath):
        with open(filepath) as file:
            for line in file:
                yield line.rstrip('\n')

    with open("/tmp/large_file.txt", "w") as f:
        f.write("Line 1\n")
        f.write("Line 2\n")
        f.write("Line 3\n")

    for line in read_large_file("/tmp/large_file.txt"):
        print(line)

    print("\nProblem 4:")
    even_squares = (x ** 2 for x in range(2, 21, 2))
    result = list(even_squares)
    print(result)

    print("\nProblem 5:")
    def batch(iterable, size):
        batch_list = []
        for item in iterable:
            batch_list.append(item)
            if len(batch_list) == size:
                yield batch_list
                batch_list = []
        if batch_list:
            yield batch_list

    for b in batch(range(1, 11), 3):
        print(b)
