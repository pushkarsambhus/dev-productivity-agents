# SOLUTIONS: Decorators
# These are reference solutions — there are often multiple valid ways to solve each problem!

import time
import math
from functools import wraps

# ===========================================================================
# Problem 1 Solution: Timer Decorator
# ===========================================================================

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Function '{func.__name__}' took {end - start:.3f} seconds")
        return result
    return wrapper

@timer
def slow_function():
    total = 0
    for i in range(1000000):
        total += i
    return total

slow_function()


# ===========================================================================
# Problem 2 Solution: Logger Decorator
# ===========================================================================

def logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling: {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Done: {func.__name__}")
        return result
    return wrapper

@logger
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")


# ===========================================================================
# Problem 3 Solution: Retry Decorator Factory
# ===========================================================================

def retry(times=3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == times:
                        raise
                    print(f"Attempt {attempt} failed")
        return wrapper
    return decorator

counter = 0

@retry(times=3)
def sometimes_fails():
    global counter
    counter += 1
    if counter < 3:
        raise Exception("Failed")
    return "Succeeded!"

result = sometimes_fails()
print(result)


# ===========================================================================
# Problem 4 Solution: Circle Class with Property Decorators
# ===========================================================================

class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value

    @property
    def area(self):
        return math.pi * self._radius ** 2

    @property
    def circumference(self):
        return 2 * math.pi * self._radius

circle = Circle(5)
print(f"Radius: {circle.radius}")
print(f"Area: {circle.area:.1f}")
print(f"Circumference: {circle.circumference:.1f}")

try:
    circle.radius = -3
except ValueError as e:
    print(e)


# ===========================================================================
# Problem 5 Solution: Validate Arguments Decorator
# ===========================================================================

def validate_positive(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        for arg in args:
            if isinstance(arg, (int, float)) and arg < 0:
                raise ValueError("Argument values cannot be negative")
        for value in kwargs.values():
            if isinstance(value, (int, float)) and value < 0:
                raise ValueError("Argument values cannot be negative")
        return func(*args, **kwargs)
    return wrapper

@validate_positive
def add(a, b):
    return a + b

print(add(3, 5))

try:
    print(add(-2, 5))
except ValueError as e:
    print(e)

try:
    print(add(2, -5))
except ValueError as e:
    print(e)


if __name__ == "__main__":
    print("=== Running all solutions ===")

    print("\nProblem 1:")
    def timer(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            print(f"Function '{func.__name__}' took {end - start:.3f} seconds")
            return result
        return wrapper

    @timer
    def slow_function():
        total = 0
        for i in range(1000000):
            total += i
        return total

    slow_function()

    print("\nProblem 2:")
    def logger(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"Calling: {func.__name__}")
            result = func(*args, **kwargs)
            print(f"Done: {func.__name__}")
            return result
        return wrapper

    @logger
    def greet(name):
        print(f"Hello, {name}!")

    greet("Alice")

    print("\nProblem 3:")
    def retry(times=3):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                for attempt in range(1, times + 1):
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        if attempt == times:
                            raise
                        print(f"Attempt {attempt} failed")
            return wrapper
        return decorator

    counter = 0

    @retry(times=3)
    def sometimes_fails():
        global counter
        counter += 1
        if counter < 3:
            raise Exception("Failed")
        return "Succeeded!"

    result = sometimes_fails()
    print(result)

    print("\nProblem 4:")
    class Circle:
        def __init__(self, radius):
            self._radius = radius

        @property
        def radius(self):
            return self._radius

        @radius.setter
        def radius(self, value):
            if value < 0:
                raise ValueError("Radius cannot be negative")
            self._radius = value

        @property
        def area(self):
            return math.pi * self._radius ** 2

        @property
        def circumference(self):
            return 2 * math.pi * self._radius

    circle = Circle(5)
    print(f"Radius: {circle.radius}")
    print(f"Area: {circle.area:.1f}")
    print(f"Circumference: {circle.circumference:.1f}")

    try:
        circle.radius = -3
    except ValueError as e:
        print(e)

    print("\nProblem 5:")
    def validate_positive(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for arg in args:
                if isinstance(arg, (int, float)) and arg < 0:
                    raise ValueError("Argument values cannot be negative")
            for value in kwargs.values():
                if isinstance(value, (int, float)) and value < 0:
                    raise ValueError("Argument values cannot be negative")
            return func(*args, **kwargs)
        return wrapper

    @validate_positive
    def add(a, b):
        return a + b

    print(add(3, 5))

    try:
        print(add(-2, 5))
    except ValueError as e:
        print(e)

    try:
        print(add(2, -5))
    except ValueError as e:
        print(e)
