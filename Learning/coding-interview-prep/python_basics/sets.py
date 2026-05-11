# A set is an unordered collection of UNIQUE items — no duplicates allowed.
# Sets are great for removing duplicates and for comparing groups of items.

fruits = {"apple", "banana", "cherry", "apple"}  # "apple" appears only once

# --- Adding and removing ---
fruits.add("mango")        # adds a new item
fruits.discard("banana")   # removes item (no error if it doesn't exist)

# --- Set operations ---
a = {1, 2, 3, 4, 5}
b = {4, 5, 6, 7, 8}

union = a | b               # all items from both sets (no duplicates)
intersection = a & b        # only items that appear in BOTH sets
difference = a - b          # items in 'a' but NOT in 'b'
symmetric_diff = a ^ b      # items in either set, but NOT in both

# --- Membership check ---
has_apple = "apple" in fruits   # True if "apple" is in the set

# --- Removing duplicates from a list using a set ---
numbers_with_dupes = [1, 2, 2, 3, 3, 3, 4]
unique_numbers = list(set(numbers_with_dupes))  # removes duplicates

if __name__ == "__main__":
    print("Fruits set:", fruits)
    print("Has apple:", has_apple)
    print("Set A:", a)
    print("Set B:", b)
    print("Union (A | B):", union)
    print("Intersection (A & B):", intersection)
    print("Difference (A - B):", difference)
    print("Symmetric difference (A ^ B):", symmetric_diff)
    print("Unique numbers:", unique_numbers)
