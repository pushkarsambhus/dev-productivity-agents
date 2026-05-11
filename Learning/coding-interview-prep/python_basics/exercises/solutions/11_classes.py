# SOLUTIONS: Classes and Objects
# These are reference solutions — there are often multiple valid ways to solve each problem!

# ===========================================================================
# Problem 1 Solution: Rectangle Class with Area and Perimeter
# ===========================================================================

class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

rect = Rectangle(5, 3)
print(f"Area: {rect.area()}")
print(f"Perimeter: {rect.perimeter()}")


# ===========================================================================
# Problem 2 Solution: is_square() Method
# ===========================================================================

class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

    def is_square(self):
        return self.width == self.height

rect1 = Rectangle(5, 3)
rect2 = Rectangle(4, 4)
print(rect1.is_square())
print(rect2.is_square())


# ===========================================================================
# Problem 3 Solution: BankAccount Class
# ===========================================================================

class BankAccount:
    def __init__(self):
        self.balance = 0

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient funds")
        else:
            self.balance -= amount

account = BankAccount()
account.deposit(100)
print(f"Current balance: {account.balance}")
account.withdraw(70)
print(f"Current balance: {account.balance}")
account.withdraw(50)


# ===========================================================================
# Problem 4 Solution: Transfer Method
# ===========================================================================

class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient funds")
            return False
        else:
            self.balance -= amount
            return True

    def transfer(self, amount, other_account):
        if self.withdraw(amount):
            other_account.deposit(amount)

account1 = BankAccount(100)
account2 = BankAccount(0)
account1.transfer(50, account2)
print(f"Account 1: {account1.balance}")
print(f"Account 2: {account2.balance}")


# ===========================================================================
# Problem 5 Solution: Counter Class
# ===========================================================================

class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1

    def decrement(self):
        self.count -= 1

    def reset(self):
        self.count = 0

    def value(self):
        return self.count

counter = Counter()
counter.increment()
print(counter.value())
counter.decrement()
print(counter.value())
counter.reset()
counter.increment()
counter.increment()
counter.increment()
counter.increment()
counter.increment()
print(counter.value())


if __name__ == "__main__":
    print("=== Running all solutions ===")

    print("\nProblem 1:")
    class Rectangle:
        def __init__(self, width, height):
            self.width = width
            self.height = height

        def area(self):
            return self.width * self.height

        def perimeter(self):
            return 2 * (self.width + self.height)

    rect = Rectangle(5, 3)
    print(f"Area: {rect.area()}")
    print(f"Perimeter: {rect.perimeter()}")

    print("\nProblem 2:")
    class Rectangle:
        def __init__(self, width, height):
            self.width = width
            self.height = height

        def area(self):
            return self.width * self.height

        def perimeter(self):
            return 2 * (self.width + self.height)

        def is_square(self):
            return self.width == self.height

    rect1 = Rectangle(5, 3)
    rect2 = Rectangle(4, 4)
    print(rect1.is_square())
    print(rect2.is_square())

    print("\nProblem 3:")
    class BankAccount:
        def __init__(self):
            self.balance = 0

        def deposit(self, amount):
            self.balance += amount

        def withdraw(self, amount):
            if amount > self.balance:
                print("Insufficient funds")
            else:
                self.balance -= amount

    account = BankAccount()
    account.deposit(100)
    print(f"Current balance: {account.balance}")
    account.withdraw(70)
    print(f"Current balance: {account.balance}")
    account.withdraw(50)

    print("\nProblem 4:")
    class BankAccount:
        def __init__(self, balance=0):
            self.balance = balance

        def deposit(self, amount):
            self.balance += amount

        def withdraw(self, amount):
            if amount > self.balance:
                print("Insufficient funds")
                return False
            else:
                self.balance -= amount
                return True

        def transfer(self, amount, other_account):
            if self.withdraw(amount):
                other_account.deposit(amount)

    account1 = BankAccount(100)
    account2 = BankAccount(0)
    account1.transfer(50, account2)
    print(f"Account 1: {account1.balance}")
    print(f"Account 2: {account2.balance}")

    print("\nProblem 5:")
    class Counter:
        def __init__(self):
            self.count = 0

        def increment(self):
            self.count += 1

        def decrement(self):
            self.count -= 1

        def reset(self):
            self.count = 0

        def value(self):
            return self.count

    counter = Counter()
    counter.increment()
    print(counter.value())
    counter.decrement()
    print(counter.value())
    counter.reset()
    counter.increment()
    counter.increment()
    counter.increment()
    counter.increment()
    counter.increment()
    print(counter.value())
