# Error handling lets your program deal with problems gracefully instead of crashing.
# try: attempt something that might fail
# except: handle specific errors if they occur
# else: runs ONLY if no error occurred in try
# finally: ALWAYS runs, regardless of success or failure

def divide(a, b):
    return a / b   # this will crash if b is 0 (ZeroDivisionError)

def parse_number(text):
    return int(text)   # crashes if text isn't a valid number (ValueError)

def get_item(my_list, index):
    return my_list[index]   # crashes if index is out of range (IndexError)

if __name__ == "__main__":
    # --- Example 1: catching a specific error ---
    print("--- Division ---")
    try:
        result = divide(10, 0)    # this will fail
    except ZeroDivisionError:
        print("Error: Cannot divide by zero!")
    else:
        print("Result:", result)   # only runs if no error
    finally:
        print("Division attempt complete.\n")   # always runs

    # --- Example 2: multiple except blocks ---
    print("--- Parsing ---")
    for text in ["42", "hello", "3.14"]:
        try:
            number = parse_number(text)
            print(f"Parsed '{text}' → {number}")
        except ValueError as e:
            print(f"Could not parse '{text}': {e}")

    # --- Example 3: catching multiple error types in one block ---
    print("\n--- List Access ---")
    data = [10, 20, 30]
    for index in [1, 5, "two"]:
        try:
            value = get_item(data, index)
            print(f"Item at {index}: {value}")
        except (IndexError, TypeError) as e:
            print(f"Error accessing index {index}: {e}")

    # --- Example 4: catching ANY exception (use sparingly) ---
    print("\n--- Catch-all ---")
    try:
        result = 10 / 2
        print("Success:", result)
    except Exception as e:
        print("Something went wrong:", e)
    finally:
        print("Always runs.")
