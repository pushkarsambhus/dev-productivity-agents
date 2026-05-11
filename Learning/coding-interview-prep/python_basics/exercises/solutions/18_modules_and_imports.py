# SOLUTIONS: Modules and Standard Library
# These are reference solutions — there are often multiple valid ways to solve each problem!

import math
import random
from datetime import datetime, timedelta
import os
from collections import Counter

# ===========================================================================
# Problem 1 Solution: Math Module
# ===========================================================================

hypotenuse = math.sqrt(3**2 + 4**2)
floor_val = math.floor(7.3)
ceil_val = math.ceil(7.3)
log_val = math.log2(64)

print(f"Hypotenuse: {hypotenuse}")
print(f"Floor: {floor_val}")
print(f"Ceiling: {ceil_val}")
print(f"Log base 2: {log_val}")


# ===========================================================================
# Problem 2 Solution: Random Module - Dice Rolling
# ===========================================================================

sevens_count = 0
for i in range(10):
    die1 = random.randint(1, 6)
    die2 = random.randint(1, 6)
    total = die1 + die2
    print(f"Roll {i+1}: ({die1}, {die2}) = {total}")
    if total == 7:
        sevens_count += 1

print(f"Total 7s: {sevens_count}")


# ===========================================================================
# Problem 3 Solution: Datetime Module
# ===========================================================================

today = datetime.now()
print(f"Today: {today.date()}")

# Days until next New Year
next_year = datetime(today.year + 1, 1, 1)
days_until_new_year = (next_year - today).days
print(f"Days until New Year: {days_until_new_year}")

# Days since Jan 1, 2000
birth_date = datetime(2000, 1, 1)
age_in_days = (today - birth_date).days
print(f"Days since Jan 1, 2000: {age_in_days}")


# ===========================================================================
# Problem 4 Solution: OS Module
# ===========================================================================

current_dir = os.getcwd()
print(f"Current directory: {current_dir}")

tmp_exists = os.path.exists("/tmp")
print(f"/tmp exists: {tmp_exists}")

items = os.listdir("/tmp")[:5]
print("First 5 items in /tmp:")
for item in items:
    print(item)


# ===========================================================================
# Problem 5 Solution: Collections.Counter
# ===========================================================================

sentence = "to be or not to be that is the question"
words = sentence.split()
word_count = Counter(words)

print("Word frequencies:")
for word, count in word_count.most_common(5):
    print(f"{word}: {count}")


if __name__ == "__main__":
    print("=== Running all solutions ===")

    print("\nProblem 1:")
    hypotenuse = math.sqrt(3**2 + 4**2)
    floor_val = math.floor(7.3)
    ceil_val = math.ceil(7.3)
    log_val = math.log2(64)
    print(f"Hypotenuse: {hypotenuse}")
    print(f"Floor: {floor_val}")
    print(f"Ceiling: {ceil_val}")
    print(f"Log base 2: {log_val}")

    print("\nProblem 2:")
    sevens_count = 0
    for i in range(10):
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        total = die1 + die2
        print(f"Roll {i+1}: ({die1}, {die2}) = {total}")
        if total == 7:
            sevens_count += 1
    print(f"Total 7s: {sevens_count}")

    print("\nProblem 3:")
    today = datetime.now()
    print(f"Today: {today.date()}")
    next_year = datetime(today.year + 1, 1, 1)
    days_until_new_year = (next_year - today).days
    print(f"Days until New Year: {days_until_new_year}")
    birth_date = datetime(2000, 1, 1)
    age_in_days = (today - birth_date).days
    print(f"Days since Jan 1, 2000: {age_in_days}")

    print("\nProblem 4:")
    current_dir = os.getcwd()
    print(f"Current directory: {current_dir}")
    tmp_exists = os.path.exists("/tmp")
    print(f"/tmp exists: {tmp_exists}")
    items = os.listdir("/tmp")[:5]
    print("First 5 items in /tmp:")
    for item in items:
        print(item)

    print("\nProblem 5:")
    sentence = "to be or not to be that is the question"
    words = sentence.split()
    word_count = Counter(words)
    print("Word frequencies:")
    for word, count in word_count.most_common(5):
        print(f"{word}: {count}")
