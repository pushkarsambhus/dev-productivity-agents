# A module is just a Python file that contains code you can reuse.
# Python's standard library comes with lots of built-in modules.
# You can also import code you've written in other files.

# --- Importing standard library modules ---
import math          # math functions like sqrt, pi, floor
import random        # generating random numbers
import datetime      # working with dates and times
import os            # interacting with the operating system

# --- Selective import: only bring in what you need ---
from math import sqrt, pi    # now you can use sqrt() directly instead of math.sqrt()

# --- Aliased import: give a module a shorter nickname ---
import datetime as dt

if __name__ == "__main__":
    # math module
    print("Pi:", math.pi)
    print("Square root of 144:", math.sqrt(144))
    print("Floor of 9.7:", math.floor(9.7))
    print("Direct sqrt import:", sqrt(25))

    # random module
    print("\nRandom number (1–10):", random.randint(1, 10))
    fruits = ["apple", "banana", "cherry"]
    print("Random fruit:", random.choice(fruits))

    # datetime module
    today = dt.date.today()
    print("\nToday's date:", today)
    print("Year:", today.year, "| Month:", today.month, "| Day:", today.day)

    # os module
    print("\nCurrent directory:", os.getcwd())
    print("Does /tmp exist?", os.path.exists("/tmp"))
