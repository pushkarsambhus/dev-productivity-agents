# SOLUTIONS: Error Handling
# These are reference solutions — there are often multiple valid ways to solve each problem!

# ===========================================================================
# Problem 1 Solution: Safe Division
# ===========================================================================

def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None

print(safe_divide(4, 2))
print(safe_divide(4, 0))
print(safe_divide(0, 0))


# ===========================================================================
# Problem 2 Solution: Safe Type Conversion
# ===========================================================================

def safe_convert(value, type_fn):
    try:
        return type_fn(value)
    except (ValueError, TypeError):
        return None

print(safe_convert("42", int))
print(safe_convert("hello", int))
print(safe_convert("3.14", float))
print(safe_convert("abc", float))


# ===========================================================================
# Problem 3 Solution: File Reading with Finally
# ===========================================================================

def read_file_safely(filename):
    try:
        with open(filename, "r") as f:
            return f.read()
    except FileNotFoundError:
        print(f"File {filename} not found")
    finally:
        print("Attempt complete")

read_file_safely("/tmp/missing.txt")


# ===========================================================================
# Problem 4 Solution: Multiple Exception Types
# ===========================================================================

def process_numbers(values):
    try:
        total = sum(int(v) for v in values)
        return total
    except IndexError:
        print("Cannot access empty list")
    except TypeError:
        print("All values must be numeric")
    except ValueError:
        print("Cannot convert to number")

process_numbers([])
process_numbers([1, "two", 3])
process_numbers(["a", "b", "c"])


# ===========================================================================
# Problem 5 Solution: try/except/else/finally Complete Example
# ===========================================================================

def demonstrate_all_blocks(should_fail):
    try:
        if should_fail:
            raise ValueError("Intentional error")
        result = 10 / 2
    except ValueError:
        print("Error occurred")
    else:
        print("Success!")
    finally:
        print("Done.")

demonstrate_all_blocks(False)
demonstrate_all_blocks(True)


if __name__ == "__main__":
    print("=== Running all solutions ===")

    print("\nProblem 1:")
    def safe_divide(a, b):
        try:
            return a / b
        except ZeroDivisionError:
            return None

    print(safe_divide(4, 2))
    print(safe_divide(4, 0))
    print(safe_divide(0, 0))

    print("\nProblem 2:")
    def safe_convert(value, type_fn):
        try:
            return type_fn(value)
        except (ValueError, TypeError):
            return None

    print(safe_convert("42", int))
    print(safe_convert("hello", int))
    print(safe_convert("3.14", float))
    print(safe_convert("abc", float))

    print("\nProblem 3:")
    def read_file_safely(filename):
        try:
            with open(filename, "r") as f:
                return f.read()
        except FileNotFoundError:
            print(f"File {filename} not found")
        finally:
            print("Attempt complete")

    read_file_safely("/tmp/missing.txt")

    print("\nProblem 4:")
    def process_numbers(values):
        try:
            total = sum(int(v) for v in values)
            return total
        except IndexError:
            print("Cannot access empty list")
        except TypeError:
            print("All values must be numeric")
        except ValueError:
            print("Cannot convert to number")

    process_numbers([])
    process_numbers([1, "two", 3])
    process_numbers(["a", "b", "c"])

    print("\nProblem 5:")
    def demonstrate_all_blocks(should_fail):
        try:
            if should_fail:
                raise ValueError("Intentional error")
            result = 10 / 2
        except ValueError:
            print("Error occurred")
        else:
            print("Success!")
        finally:
            print("Done.")

    demonstrate_all_blocks(False)
    demonstrate_all_blocks(True)
