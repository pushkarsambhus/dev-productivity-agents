# Encapsulation means hiding the internal details of a class from the outside.
# Public attributes: anyone can access them (normal names like self.name)
# Protected attributes: "please don't touch" signal — one underscore: self._age
# Private attributes: truly hidden — two underscores: self.__password
# Getters/setters: controlled ways to read and change protected/private data.

class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner             # PUBLIC: anyone can access this freely
        self._account_type = "savings" # PROTECTED: meant for internal/subclass use
        self.__balance = balance        # PRIVATE: hidden from outside the class

    # Getter: a safe way to READ the private balance
    @property
    def balance(self):
        return self.__balance

    # Setter: a safe way to CHANGE the private balance (with validation)
    @balance.setter
    def balance(self, amount):
        if amount < 0:
            print("Error: Balance cannot be negative.")
        else:
            self.__balance = amount

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            print(f"Deposited ${amount}. New balance: ${self.__balance}")

    def withdraw(self, amount):
        if amount > self.__balance:
            print("Insufficient funds.")
        else:
            self.__balance -= amount
            print(f"Withdrew ${amount}. New balance: ${self.__balance}")

if __name__ == "__main__":
    account = BankAccount("Alice", 1000)

    print("Owner:", account.owner)                 # public — works fine
    print("Account type:", account._account_type)  # protected — works but discouraged
    print("Balance:", account.balance)             # uses getter

    account.deposit(500)
    account.withdraw(200)
    account.balance = 5000    # uses setter
    print("Updated balance:", account.balance)
    account.balance = -100    # setter blocks this
