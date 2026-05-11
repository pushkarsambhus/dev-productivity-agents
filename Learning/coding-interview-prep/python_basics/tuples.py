# A tuple is like a list, but it CANNOT be changed once created (immutable).
# Use tuples for data that should stay fixed, like coordinates or RGB colors.

coordinates = (10, 20)          # a simple tuple with two values
rgb_color = (255, 128, 0)       # red, green, blue values for orange
mixed = (42, "hello", True)     # tuples can hold different types

# --- Accessing items (same as lists, using index) ---
x = coordinates[0]   # 10
y = coordinates[1]   # 20

# --- Unpacking: assigning tuple values to individual variables in one step ---
red, green, blue = rgb_color   # red=255, green=128, blue=0

# --- Tuples with one item need a trailing comma ---
single_item = (99,)   # without the comma, Python treats it as just parentheses

# --- You can convert between tuple and list ---
as_list = list(coordinates)    # (10, 20) → [10, 20]  (now changeable)
back_to_tuple = tuple(as_list) # [10, 20] → (10, 20)  (fixed again)

if __name__ == "__main__":
    print("Coordinates:", coordinates)
    print("X:", x, "Y:", y)
    print("RGB unpacked — Red:", red, "Green:", green, "Blue:", blue)
    print("Single item tuple:", single_item)
    print("As list:", as_list)
    print("Mixed tuple:", mixed)
    print("Tuple length:", len(rgb_color))
