# Practice: Inheritance
# In these exercises you will practice: base classes, inheritance, method overriding, super(), and multiple inheritance

# ===========================================================================
# Problem 1: Vehicle Base Class
# ===========================================================================
# Create a Vehicle base class with make, model, year attributes.
# Add a description() method that returns "2020 Toyota Camry"
# Create Car(Vehicle) that adds num_doors, and Motorcycle(Vehicle) that adds has_sidecar.
# Test both.

# YOUR CODE HERE

# Expected output:
# 2020 Toyota Camry
# 2019 Harley-Davidson Street 750


# ===========================================================================
# Problem 2: Override description() Method
# ===========================================================================
# Override description() in Car to return "2020 Toyota Camry (4 doors)"
# Override description() in Motorcycle to return "2019 Harley-Davidson Street 750 (no sidecar)"

# YOUR CODE HERE

# Expected output:
# 2020 Toyota Camry (4 doors)
# 2019 Harley-Davidson Street 750 (no sidecar)


# ===========================================================================
# Problem 3: Use super() in Car
# ===========================================================================
# Modify Car's __init__ to use super() to call Vehicle's __init__,
# then add num_doors. Show that the vehicle still works correctly.

# YOUR CODE HERE

# Expected output:
# 2020 Toyota Camry (4 doors)


# ===========================================================================
# Problem 4: Multiple Inheritance - Flyable Mixin
# ===========================================================================
# Create a Flyable mixin class with a fly() method that returns "Flying through the sky..."
# Create FlyingCar(Car, Flyable) using multiple inheritance.
# Test that it has both car and flying capabilities.

# YOUR CODE HERE

# Expected output:
# 2020 Toyota Camry (4 doors)
# Flying through the sky...


# ===========================================================================
# Problem 5: Polymorphism with Mixed Objects
# ===========================================================================
# Create a list with one Car, one Motorcycle, and one FlyingCar.
# Loop through and call description() on each to show polymorphism.
# Also call fly() on the FlyingCar to show it has both behaviors.

# YOUR CODE HERE

# Expected output:
# 2020 Toyota Camry (4 doors)
# 2019 Harley-Davidson Street 750 (no sidecar)
# 2021 Tesla Model 3 (2 doors)
# Flying through the sky...


if __name__ == "__main__":
    print("Run the code above each problem to test it!")
    print("Compare your output to the '# Expected output:' comments.")
