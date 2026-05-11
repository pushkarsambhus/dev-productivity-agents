# Practice: Classes and Objects
# In these exercises you will practice: class definition, attributes, methods, and instance variables

# ===========================================================================
# Problem 1: Rectangle Class with Area and Perimeter
# ===========================================================================
# Create a Rectangle class with:
# - width and height attributes
# - area() method that returns width * height
# - perimeter() method that returns 2 * (width + height)
# Test with a rectangle of width 5 and height 3.

# YOUR CODE HERE

# Expected output:
# Area: 15
# Perimeter: 16


# ===========================================================================
# Problem 2: is_square() Method
# ===========================================================================
# Add an is_square() method to the Rectangle class that returns True
# if width == height, False otherwise.
# Test with width=5, height=3 and width=4, height=4.

# YOUR CODE HERE

# Expected output:
# False
# True


# ===========================================================================
# Problem 3: BankAccount Class
# ===========================================================================
# Create a BankAccount class with:
# - balance attribute (starting at 0)
# - deposit(amount) method
# - withdraw(amount) method (print "Insufficient funds" if not enough balance)
# Test deposits and withdrawals.

# YOUR CODE HERE

# Expected output:
# Current balance: 100
# Current balance: 30
# Insufficient funds


# ===========================================================================
# Problem 4: Transfer Method
# ===========================================================================
# Add a transfer(amount, other_account) method to BankAccount that moves
# money from one account to another.
# Test transferring $50 from account1 (balance 100) to account2 (balance 0).

# YOUR CODE HERE

# Expected output:
# Account 1: 50
# Account 2: 50


# ===========================================================================
# Problem 5: Counter Class
# ===========================================================================
# Create a Counter class with:
# - count attribute (starting at 0)
# - increment() method
# - decrement() method
# - reset() method
# - value() method (returns current count)
# Test incrementing, decrementing, and checking value.

# YOUR CODE HERE

# Expected output:
# 1
# 0
# 5


if __name__ == "__main__":
    print("Run the code above each problem to test it!")
    print("Compare your output to the '# Expected output:' comments.")
