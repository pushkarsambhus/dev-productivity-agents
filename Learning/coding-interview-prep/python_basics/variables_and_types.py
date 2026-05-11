# Variables are like labeled boxes that store information.
# Python has several built-in types: integers, floats, strings, and booleans.

# An integer is a whole number (no decimal point)
age = 25

# A float is a number with a decimal point
price = 9.99

# A string is text, wrapped in quotes
name = "Alice"

# A boolean is either True or False
is_student = True

# Type casting: converting one type to another
age_as_string = str(age)       # turns the number 25 into the text "25"
price_as_int = int(price)      # turns 9.99 into 9 (drops the decimal)
number_from_text = float("3.14")  # turns the text "3.14" into a float

if __name__ == "__main__":
    print("Age:", age, "| Type:", type(age))
    print("Price:", price, "| Type:", type(price))
    print("Name:", name, "| Type:", type(name))
    print("Is student:", is_student, "| Type:", type(is_student))
    print("Age as string:", age_as_string, "| Type:", type(age_as_string))
    print("Price as int:", price_as_int)
    print("Number from text:", number_from_text)
