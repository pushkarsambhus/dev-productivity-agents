# Conditionals let your program make decisions based on whether something is True or False.
# Think of it like: "IF this is true, do this; OTHERWISE, do that."

temperature = 75

# --- Basic if/elif/else ---
if temperature > 90:
    weather = "hot"          # runs only if temperature > 90
elif temperature > 60:
    weather = "warm"         # runs if above is False AND this is True
else:
    weather = "cold"         # runs if ALL above conditions are False

# --- Comparison operators ---
# ==  equal to
# !=  not equal to
# >   greater than
# <   less than
# >=  greater than or equal to
# <=  less than or equal to

# --- Logical operators: combining conditions ---
is_weekend = True
has_plans = False

if is_weekend and not has_plans:
    activity = "free day!"    # both must be true (and not plans = plans is False)
else:
    activity = "busy"

# --- Ternary operator: a one-line shortcut for simple if/else ---
age = 20
status = "adult" if age >= 18 else "minor"   # reads like plain English

if __name__ == "__main__":
    print(f"Temperature is {temperature}°F — it's {weather}.")
    print("Activity:", activity)
    print("Status:", status)

    # Checking multiple conditions
    score = 85
    if score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    elif score >= 70:
        grade = "C"
    else:
        grade = "F"
    print(f"Score: {score} → Grade: {grade}")
