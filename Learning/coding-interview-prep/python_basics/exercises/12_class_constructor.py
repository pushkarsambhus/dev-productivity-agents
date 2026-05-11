# Practice: Class Constructors and Special Methods
# In these exercises you will practice: __init__, __str__, __repr__, class variables, and properties

# ===========================================================================
# Problem 1: __str__ and __repr__ Methods
# ===========================================================================
# Create a Person class with __init__(name, age).
# Implement __str__ returning "Person: Alice (30)"
# Implement __repr__ returning "Person('Alice', 30)"
# Test both.

# YOUR CODE HERE

# Expected output:
# Person: Alice (30)
# Person('Alice', 30)


# ===========================================================================
# Problem 2: Class Variable - Population Counter
# ===========================================================================
# Add a class variable population = 0 to the Person class.
# Increment it each time a new Person is created.
# Create 3 people and print the population after each creation.

# YOUR CODE HERE

# Expected output:
# 1
# 2
# 3


# ===========================================================================
# Problem 3: Temperature Class with Properties
# ===========================================================================
# Create a Temperature class that stores Celsius.
# Add @property for fahrenheit and kelvin that auto-convert.
# Create a temperature of 0°C and print its Fahrenheit and Kelvin.

# YOUR CODE HERE

# Expected output:
# 32.0
# 273.15


# ===========================================================================
# Problem 4: Temperature Equality
# ===========================================================================
# Add an __eq__ method to Temperature so two Temperature objects
# are equal if they represent the same Celsius value.
# Test: Temperature(0) == Temperature(0) should be True

# YOUR CODE HERE

# Expected output:
# True
# False


# ===========================================================================
# Problem 5: Vector2D Class
# ===========================================================================
# Create a Vector2D class with x and y attributes.
# Implement __str__ returning "(3, 4)"
# Implement __repr__ returning "Vector2D(3, 4)"
# Implement magnitude() method returning sqrt(x^2 + y^2)

import math

# YOUR CODE HERE

# Expected output:
# (3, 4)
# Vector2D(3, 4)
# 5.0


if __name__ == "__main__":
    print("Run the code above each problem to test it!")
    print("Compare your output to the '# Expected output:' comments.")
