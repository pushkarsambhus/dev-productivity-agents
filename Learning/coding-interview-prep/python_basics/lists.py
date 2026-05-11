# A list is an ordered collection of items that can be changed.
# Lists can hold items of different types and allow duplicates.

fruits = ["apple", "banana", "cherry"]

# --- Adding and removing items ---
fruits.append("mango")         # adds item to the end
fruits.insert(1, "blueberry")  # inserts at position 1
fruits.remove("banana")        # removes the first occurrence of "banana"
popped = fruits.pop()          # removes and returns the last item

# --- Slicing: getting a portion of the list ---
first_two = fruits[0:2]   # items at index 0 and 1
reversed_list = fruits[::-1]  # reverses the entire list

# --- Useful list operations ---
numbers = [3, 1, 4, 1, 5, 9, 2, 6]
sorted_numbers = sorted(numbers)   # returns a new sorted list
numbers.sort()                     # sorts the list in place
total = sum(numbers)               # adds all numbers together
length = len(fruits)               # counts number of items

# --- List comprehension: creating a new list using a compact expression ---
squares = [x ** 2 for x in range(1, 6)]  # [1, 4, 9, 16, 25]

if __name__ == "__main__":
    print("Fruits:", fruits)
    print("Popped item:", popped)
    print("First two:", first_two)
    print("Reversed:", reversed_list)
    print("Sorted numbers:", sorted_numbers)
    print("Sum:", total)
    print("List length:", length)
    print("Squares:", squares)
