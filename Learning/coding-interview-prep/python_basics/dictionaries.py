# A dictionary stores data as key-value pairs, like a real dictionary (word → definition).
# Keys must be unique; values can be anything.

person = {
    "name": "Alice",
    "age": 30,
    "city": "New York"
}

# --- Accessing values ---
name = person["name"]              # direct access by key
age = person.get("age")            # safer access (returns None if key missing)
missing = person.get("email", "N/A")  # returns "N/A" if "email" doesn't exist

# --- Adding and updating entries ---
person["email"] = "alice@example.com"  # adds a new key
person["age"] = 31                     # updates an existing key

# --- Removing entries ---
removed = person.pop("city")       # removes "city" and returns its value

# --- Looping through a dictionary ---
# .keys() gives all keys, .values() gives all values, .items() gives both

# --- Dict comprehension: build a dict from an expression ---
squares = {x: x ** 2 for x in range(1, 6)}  # {1:1, 2:4, 3:9, 4:16, 5:25}

if __name__ == "__main__":
    print("Person:", person)
    print("Name:", name)
    print("Age:", age)
    print("Missing key result:", missing)
    print("Removed city:", removed)
    print("\nLooping through keys and values:")
    for key, value in person.items():
        print(f"  {key}: {value}")
    print("Squares dict:", squares)
