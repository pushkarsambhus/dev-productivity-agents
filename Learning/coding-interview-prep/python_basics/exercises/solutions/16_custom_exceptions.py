# SOLUTIONS: Custom Exceptions
# These are reference solutions — there are often multiple valid ways to solve each problem!

# ===========================================================================
# Problem 1 Solution: ValidationError Exception
# ===========================================================================

class ValidationError(Exception):
    pass

def validate_age(age):
    if age < 0:
        raise ValidationError("Age cannot be negative")
    if age > 150:
        raise ValidationError("Age cannot be greater than 150")
    return True

try:
    validate_age(25)
    print("Age is valid")
except ValidationError as e:
    print(e)

try:
    validate_age(-5)
except ValidationError as e:
    print(e)

try:
    validate_age(200)
except ValidationError as e:
    print(e)


# ===========================================================================
# Problem 2 Solution: Multiple Custom Exceptions
# ===========================================================================

class InsufficientFundsError(Exception):
    pass

class NegativeAmountError(Exception):
    pass

def withdraw(balance, amount):
    if amount < 0:
        raise NegativeAmountError("Amount cannot be negative")
    if amount > balance:
        raise InsufficientFundsError("Insufficient funds")
    return balance - amount

try:
    withdraw(100, -10)
except NegativeAmountError as e:
    print(e)

try:
    withdraw(100, 150)
except InsufficientFundsError as e:
    print(e)

try:
    result = withdraw(100, 50)
    print(f"New balance: {result}")
except (NegativeAmountError, InsufficientFundsError) as e:
    print(e)


# ===========================================================================
# Problem 3 Solution: FileReadError Exception
# ===========================================================================

class FileReadError(Exception):
    pass

def read_file(filename):
    import os
    if not os.path.exists(filename):
        raise FileReadError(f"File not found: {filename}")
    return "File contents"

try:
    read_file("nonexistent.txt")
except FileReadError as e:
    print(e)


# ===========================================================================
# Problem 4 Solution: try/except/else/finally
# ===========================================================================

class ValidationError(Exception):
    pass

def validate_age(age):
    if age < 0:
        raise ValidationError("Age cannot be negative")
    if age > 150:
        raise ValidationError("Age cannot be greater than 150")
    return True

# Test with -1
try:
    validate_age(-1)
except ValidationError as e:
    print(e)
finally:
    print("Validation attempt complete")

# Test with 200
try:
    validate_age(200)
except ValidationError as e:
    print(e)
finally:
    print("Validation attempt complete")

# Test with 25
try:
    validate_age(25)
except ValidationError as e:
    print(e)
else:
    print("Success!")
finally:
    print("Validation attempt complete")


# ===========================================================================
# Problem 5 Solution: Exception Hierarchy
# ===========================================================================

class AppError(Exception):
    pass

class DatabaseError(AppError):
    pass

class ConnectionError(DatabaseError):
    pass

try:
    raise ConnectionError("Database connection failed")
except ConnectionError as e:
    print("Caught ConnectionError")

try:
    raise ConnectionError("Database connection failed")
except DatabaseError as e:
    print("Caught DatabaseError")

try:
    raise ConnectionError("Database connection failed")
except AppError as e:
    print("Caught AppError")


if __name__ == "__main__":
    print("=== Running all solutions ===")

    print("\nProblem 1:")
    class ValidationError(Exception):
        pass

    def validate_age(age):
        if age < 0:
            raise ValidationError("Age cannot be negative")
        if age > 150:
            raise ValidationError("Age cannot be greater than 150")
        return True

    try:
        validate_age(25)
        print("Age is valid")
    except ValidationError as e:
        print(e)

    try:
        validate_age(-5)
    except ValidationError as e:
        print(e)

    try:
        validate_age(200)
    except ValidationError as e:
        print(e)

    print("\nProblem 2:")
    class InsufficientFundsError(Exception):
        pass

    class NegativeAmountError(Exception):
        pass

    def withdraw(balance, amount):
        if amount < 0:
            raise NegativeAmountError("Amount cannot be negative")
        if amount > balance:
            raise InsufficientFundsError("Insufficient funds")
        return balance - amount

    try:
        withdraw(100, -10)
    except NegativeAmountError as e:
        print(e)

    try:
        withdraw(100, 150)
    except InsufficientFundsError as e:
        print(e)

    try:
        result = withdraw(100, 50)
        print(f"New balance: {result}")
    except (NegativeAmountError, InsufficientFundsError) as e:
        print(e)

    print("\nProblem 3:")
    class FileReadError(Exception):
        pass

    def read_file(filename):
        import os
        if not os.path.exists(filename):
            raise FileReadError(f"File not found: {filename}")
        return "File contents"

    try:
        read_file("nonexistent.txt")
    except FileReadError as e:
        print(e)

    print("\nProblem 4:")
    class ValidationError(Exception):
        pass

    def validate_age(age):
        if age < 0:
            raise ValidationError("Age cannot be negative")
        if age > 150:
            raise ValidationError("Age cannot be greater than 150")
        return True

    try:
        validate_age(-1)
    except ValidationError as e:
        print(e)
    finally:
        print("Validation attempt complete")

    try:
        validate_age(200)
    except ValidationError as e:
        print(e)
    finally:
        print("Validation attempt complete")

    try:
        validate_age(25)
    except ValidationError as e:
        print(e)
    else:
        print("Success!")
    finally:
        print("Validation attempt complete")

    print("\nProblem 5:")
    class AppError(Exception):
        pass

    class DatabaseError(AppError):
        pass

    class ConnectionError(DatabaseError):
        pass

    try:
        raise ConnectionError("Database connection failed")
    except ConnectionError as e:
        print("Caught ConnectionError")

    try:
        raise ConnectionError("Database connection failed")
    except DatabaseError as e:
        print("Caught DatabaseError")

    try:
        raise ConnectionError("Database connection failed")
    except AppError as e:
        print("Caught AppError")
