# Practice: Encapsulation
# In these exercises you will practice: public/protected/private attributes, @property decorator, and getters/setters

# ===========================================================================
# Problem 1: Public, Protected, and Private Attributes
# ===========================================================================
# Create a Person class with:
# - public name attribute
# - protected _email attribute (single underscore)
# - private __ssn attribute (double underscore)
# Show how to access each and demonstrate name mangling for private attributes.

# YOUR CODE HERE

# Expected output:
# Alice
# alice@example.com
# Person__ssn


# ===========================================================================
# Problem 2: Email Property with Validation
# ===========================================================================
# Add a @property getter for _email and a setter that validates it contains "@".
# If invalid, raise ValueError with message "Invalid email format"
# Test setting a valid and invalid email.

# YOUR CODE HERE

# Expected output:
# alice@example.com
# Invalid email format


# ===========================================================================
# Problem 3: TemperatureSensor with Private Celsius
# ===========================================================================
# Create a TemperatureSensor class with private __celsius attribute.
# Add a temperature property with:
# - getter that returns __celsius
# - setter that rejects values below -273.15 (absolute zero)
# Test setting valid and invalid temperatures.

# YOUR CODE HERE

# Expected output:
# 20
# Temperature cannot be below -273.15


# ===========================================================================
# Problem 4: Temperature Status Property
# ===========================================================================
# Add a read-only status property that returns:
# - "freezing" if < 0
# - "cold" if 0-15
# - "warm" if 16-25
# - "hot" if > 25
# Test with different temperatures.

# YOUR CODE HERE

# Expected output:
# freezing
# cold
# warm
# hot


# ===========================================================================
# Problem 5: Counter with Private Count
# ===========================================================================
# Create a Counter class with:
# - private __count attribute (starts at 0)
# - increment() method
# - decrement() method (don't go below 0)
# - reset() method
# - read-only count property (getter only, no setter)
# Test incrementing and trying to modify count directly.

# YOUR CODE HERE

# Expected output:
# 1
# 0
# Cannot set attribute


if __name__ == "__main__":
    print("Run the code above each problem to test it!")
    print("Compare your output to the '# Expected output:' comments.")
