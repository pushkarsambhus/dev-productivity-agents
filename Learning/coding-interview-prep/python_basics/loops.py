# Loops let you repeat actions without writing the same code over and over.
# Python has two main types: 'for' loops (repeat a set number of times)
# and 'while' loops (repeat as long as a condition is true).

# --- For loop: go through each item in a list ---
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print("Fruit:", fruit)   # prints each fruit one at a time

# --- Range: loop a specific number of times ---
for i in range(5):           # 0, 1, 2, 3, 4
    print("Count:", i)

# --- While loop: keep going until condition is False ---
counter = 0
while counter < 3:
    print("Counter:", counter)
    counter += 1             # increases counter by 1 each time (prevents infinite loop)

# --- Break: stop the loop early ---
for num in range(10):
    if num == 5:
        break                # exits the loop when num reaches 5
    print("Num:", num)

# --- Continue: skip the current step and move to the next ---
for num in range(6):
    if num == 3:
        continue             # skips printing 3, continues with 4, 5
    print("Kept:", num)

# --- Enumerate: loop with an index counter ---
colors = ["red", "green", "blue"]
for index, color in enumerate(colors):
    print(f"  {index}: {color}")

# --- Zip: loop through two lists at the same time ---
names = ["Alice", "Bob", "Carol"]
scores = [95, 82, 78]

if __name__ == "__main__":
    print("--- For loop ---")
    for fruit in fruits:
        print(" ", fruit)

    print("--- While loop ---")
    counter = 0
    while counter < 3:
        print("  Counter:", counter)
        counter += 1

    print("--- Enumerate ---")
    for index, color in enumerate(colors):
        print(f"  {index}: {color}")

    print("--- Zip ---")
    for name, score in zip(names, scores):
        print(f"  {name} scored {score}")
