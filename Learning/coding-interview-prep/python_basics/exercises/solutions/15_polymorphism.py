# SOLUTIONS: Polymorphism
# These are reference solutions — there are often multiple valid ways to solve each problem!

import math

# ===========================================================================
# Problem 1 Solution: Shape Base Class with Overriding
# ===========================================================================

class Shape:
    def area(self):
        return 0

    def perimeter(self):
        return 0

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2

    def perimeter(self):
        return 2 * math.pi * self.radius

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

circle = Circle(5)
print(f"Circle area: {circle.area():.1f}")
print(f"Circle perimeter: {circle.perimeter():.1f}")

rect = Rectangle(4, 5)
print(f"Rectangle area: {rect.area()}")
print(f"Rectangle perimeter: {rect.perimeter()}")


# ===========================================================================
# Problem 2 Solution: Polymorphic total_area Function
# ===========================================================================

def total_area(shapes):
    return sum(shape.area() for shape in shapes)

shapes = [Circle(5), Rectangle(4, 5)]
print(f"Total area: {total_area(shapes):.1f}")


# ===========================================================================
# Problem 3 Solution: Duck Typing - Animal speak() Methods
# ===========================================================================

class Dog:
    def speak(self):
        return "Woof!"

class Cat:
    def speak(self):
        return "Meow!"

class Bird:
    def speak(self):
        return "Tweet!"

def make_noise(animals):
    for animal in animals:
        print(animal.speak())

animals = [Dog(), Cat(), Bird()]
make_noise(animals)


# ===========================================================================
# Problem 4 Solution: Logger Polymorphism
# ===========================================================================

class Logger:
    def log(self, message):
        pass

class FileLogger(Logger):
    def __init__(self):
        self.messages = []

    def log(self, message):
        self.messages.append(message)

class ConsoleLogger(Logger):
    def log(self, message):
        print(message)

console = ConsoleLogger()
console.log("Message 1")
console.log("Message 2")

file_logger = FileLogger()
file_logger.log("Message 1")
file_logger.log("Message 2")
print(file_logger.messages)


# ===========================================================================
# Problem 5 Solution: Duck Typing with Robot
# ===========================================================================

class Dog:
    def speak(self):
        return "Woof!"

class Cat:
    def speak(self):
        return "Meow!"

class Robot:
    def speak(self):
        return "beep boop"

def make_noise(entities):
    for entity in entities:
        print(entity.speak())

entities = [Dog(), Cat(), Robot()]
make_noise(entities)


if __name__ == "__main__":
    print("=== Running all solutions ===")

    print("\nProblem 1:")
    class Shape:
        def area(self):
            return 0

        def perimeter(self):
            return 0

    class Circle(Shape):
        def __init__(self, radius):
            self.radius = radius

        def area(self):
            return math.pi * self.radius ** 2

        def perimeter(self):
            return 2 * math.pi * self.radius

    class Rectangle(Shape):
        def __init__(self, width, height):
            self.width = width
            self.height = height

        def area(self):
            return self.width * self.height

        def perimeter(self):
            return 2 * (self.width + self.height)

    circle = Circle(5)
    print(f"Circle area: {circle.area():.1f}")
    print(f"Circle perimeter: {circle.perimeter():.1f}")
    rect = Rectangle(4, 5)
    print(f"Rectangle area: {rect.area()}")
    print(f"Rectangle perimeter: {rect.perimeter()}")

    print("\nProblem 2:")
    def total_area(shapes):
        return sum(shape.area() for shape in shapes)

    shapes = [Circle(5), Rectangle(4, 5)]
    print(f"Total area: {total_area(shapes):.1f}")

    print("\nProblem 3:")
    class Dog:
        def speak(self):
            return "Woof!"

    class Cat:
        def speak(self):
            return "Meow!"

    class Bird:
        def speak(self):
            return "Tweet!"

    def make_noise(animals):
        for animal in animals:
            print(animal.speak())

    animals = [Dog(), Cat(), Bird()]
    make_noise(animals)

    print("\nProblem 4:")
    class Logger:
        def log(self, message):
            pass

    class FileLogger(Logger):
        def __init__(self):
            self.messages = []

        def log(self, message):
            self.messages.append(message)

    class ConsoleLogger(Logger):
        def log(self, message):
            print(message)

    console = ConsoleLogger()
    console.log("Message 1")
    console.log("Message 2")
    file_logger = FileLogger()
    file_logger.log("Message 1")
    file_logger.log("Message 2")
    print(file_logger.messages)

    print("\nProblem 5:")
    class Dog:
        def speak(self):
            return "Woof!"

    class Cat:
        def speak(self):
            return "Meow!"

    class Robot:
        def speak(self):
            return "beep boop"

    def make_noise(entities):
        for entity in entities:
            print(entity.speak())

    entities = [Dog(), Cat(), Robot()]
    make_noise(entities)
