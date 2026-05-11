# Strings are sequences of characters (text).
# Python gives us lots of built-in tools to work with strings.

greeting = "Hello, World!"

# --- String methods ---
upper_case = greeting.upper()          # converts all letters to UPPERCASE
lower_case = greeting.lower()          # converts all letters to lowercase
replaced = greeting.replace("World", "Python")  # swaps one word for another
stripped = "  lots of spaces  ".strip()         # removes spaces from both ends
words = greeting.split(", ")           # splits string into a list at each ", "

# --- Slicing: grabbing a portion of a string ---
first_five = greeting[0:5]    # characters at positions 0, 1, 2, 3, 4
last_six = greeting[-6:]      # last 6 characters (negative index counts from end)
every_other = greeting[::2]   # every second character

# --- f-strings: the modern way to embed variables inside strings ---
name = "Alice"
score = 95
message = f"Hello, {name}! Your score is {score}."  # variables go inside {}

if __name__ == "__main__":
    print("Original:", greeting)
    print("Uppercase:", upper_case)
    print("Lowercase:", lower_case)
    print("Replaced:", replaced)
    print("Stripped:", stripped)
    print("Split into list:", words)
    print("First 5 chars:", first_five)
    print("Last 6 chars:", last_six)
    print("Every other char:", every_other)
    print("f-string message:", message)
