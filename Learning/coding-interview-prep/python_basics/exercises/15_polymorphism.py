# Practice: Polymorphism
# In these exercises you will practice: method overriding, duck typing, and polymorphic behavior

# ===========================================================================
# Problem 1: Shape Base Class with Overriding
# ===========================================================================
# Create a Shape base class with area() and perimeter() methods (return 0).
# Create Circle(radius) and Rectangle(w, h) that override both methods.
# Circle area = pi*r^2, perimeter = 2*pi*r
# Test both shapes.

import math

# YOUR CODE HERE

# Expected output:
# Circle area: 78.5
# Circle perimeter: 31.4
# Rectangle area: 20
# Rectangle perimeter: 18


# ===========================================================================
# Problem 2: Polymorphic total_area Function
# ===========================================================================
# Create a function total_area(shapes) that sums the areas of all shapes.
# Test with a list containing a Circle and a Rectangle.

# YOUR CODE HERE

# Expected output:
# Total area: 98.5


# ===========================================================================
# Problem 3: Duck Typing - Animal speak() Methods
# ===========================================================================
# Create Dog, Cat, and Bird classes each with a speak() method.
# Write a make_noise(animals) function that calls speak() on each.
# This demonstrates duck typing - doesn't care about type, just the method.

# YOUR CODE HERE

# Expected output:
# Woof!
# Meow!
# Tweet!


# ===========================================================================
# Problem 4: Logger Polymorphism
# ===========================================================================
# Create Logger base class with log(message) method.
# Create FileLogger that stores messages in a list (not actual file).
# Create ConsoleLogger that prints messages.
# Test both loggers with the same interface.

# YOUR CODE HERE

# Expected output:
# Message 1
# Message 2
# ['Message 1', 'Message 2']


# ===========================================================================
# Problem 5: Duck Typing with Robot
# ===========================================================================
# Create a Robot class with speak() method returning "beep boop".
# Pass a Robot to make_noise() from Problem 3 alongside animals.
# Show that duck typing allows any object with speak() method to work.

# YOUR CODE HERE

# Expected output:
# Woof!
# Meow!
# beep boop


if __name__ == "__main__":
    print("Run the code above each problem to test it!")
    print("Compare your output to the '# Expected output:' comments.")
