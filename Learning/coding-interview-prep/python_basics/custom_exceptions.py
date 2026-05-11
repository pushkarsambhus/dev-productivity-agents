# Custom exceptions let you create your own error types for specific situations.
# This makes error messages more meaningful and easier to handle.
# try/except/finally: "try this, catch errors if any, always run finally."

# --- Creating a custom exception (just inherit from Exception) ---
class InsufficientFundsError(Exception):
    """Raised when a withdrawal exceeds the available balance."""
    def __init__(self, amount, balance):
        self.amount = amount
        self.balance = balance
        super().__init__(f"Cannot withdraw ${amount}. Balance is only ${balance}.")

class NegativeAmountError(Exception):
    """Raised when a negative dollar amount is used."""
    pass   # no extra logic needed — the message is enough

def withdraw(balance, amount):
    if amount < 0:
        raise NegativeAmountError("Amount must be positive.")
    if amount > balance:
        raise InsufficientFundsError(amount, balance)
    return balance - amount

if __name__ == "__main__":
    current_balance = 100

    # --- Example 1: successful withdrawal ---
    try:
        new_balance = withdraw(current_balance, 40)
        print(f"Withdrawal successful! New balance: ${new_balance}")
    except InsufficientFundsError as e:
        print("Error:", e)
    finally:
        print("Transaction attempted.")   # always runs, no matter what

    print()

    # --- Example 2: withdrawal too large ---
    try:
        new_balance = withdraw(current_balance, 200)
    except InsufficientFundsError as e:
        print("Error:", e)
    except NegativeAmountError as e:
        print("Error:", e)
    finally:
        print("Transaction attempted.")

    print()

    # --- Example 3: negative amount ---
    try:
        new_balance = withdraw(current_balance, -50)
    except (InsufficientFundsError, NegativeAmountError) as e:
        print("Error:", e)
