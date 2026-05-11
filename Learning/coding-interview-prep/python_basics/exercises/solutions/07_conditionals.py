# SOLUTIONS: Conditional Statements
# These are reference solutions — there are often multiple valid ways to solve each problem!

# ===========================================================================
# Problem 1 Solution: Age Categories
# ===========================================================================

age = 17
if age >= 18:
    print("Can vote")
elif age >= 16:
    print("Can drive")
else:
    print("Minor")


# ===========================================================================
# Problem 2 Solution: Letter Grade from Score
# ===========================================================================

score = 73
if score >= 90:
    print("A")
elif score >= 80:
    print("B")
elif score >= 70:
    print("C")
elif score >= 60:
    print("D")
else:
    print("F")


# ===========================================================================
# Problem 3 Solution: Weather Recommendation
# ===========================================================================

temperature = 28
is_raining = False

if is_raining and temperature < 10:
    print("Stay indoors")
elif is_raining and temperature >= 10:
    print("Bring an umbrella")
elif not is_raining and temperature > 20:
    print("Go outside!")
elif not is_raining and temperature <= 20:
    print("Wear a jacket")


# ===========================================================================
# Problem 4 Solution: Ternary Expression - Pass or Fail
# ===========================================================================

score = 73
result = "pass" if score >= 60 else "fail"
print(f"Score: {score} - Result: {result}")


# ===========================================================================
# Problem 5 Solution: Authentication Logic
# ===========================================================================

username = "admin"
password = "secret123"
correct_username = "admin"
correct_password = "secret123"

if username == correct_username and password == correct_password:
    print("Access granted")
elif username == correct_username and password != correct_password:
    print("Wrong password")
else:
    print("Unknown user")


if __name__ == "__main__":
    print("=== Running all solutions ===")

    print("\nProblem 1:")
    age = 17
    if age >= 18:
        print("Can vote")
    elif age >= 16:
        print("Can drive")
    else:
        print("Minor")

    print("\nProblem 2:")
    score = 73
    if score >= 90:
        print("A")
    elif score >= 80:
        print("B")
    elif score >= 70:
        print("C")
    elif score >= 60:
        print("D")
    else:
        print("F")

    print("\nProblem 3:")
    temperature = 28
    is_raining = False
    if is_raining and temperature < 10:
        print("Stay indoors")
    elif is_raining and temperature >= 10:
        print("Bring an umbrella")
    elif not is_raining and temperature > 20:
        print("Go outside!")
    elif not is_raining and temperature <= 20:
        print("Wear a jacket")

    print("\nProblem 4:")
    score = 73
    result = "pass" if score >= 60 else "fail"
    print(f"Score: {score} - Result: {result}")

    print("\nProblem 5:")
    username = "admin"
    password = "secret123"
    correct_username = "admin"
    correct_password = "secret123"
    if username == correct_username and password == correct_password:
        print("Access granted")
    elif username == correct_username and password != correct_password:
        print("Wrong password")
    else:
        print("Unknown user")
