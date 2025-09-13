def divisibility(number):
    print(number)
    if number % 3 == 0 and number % 5 == 0:
        print("Number divisible by both")
    elif number % 3 == 0:
        print("Number divisible by 3")
    elif number % 5 == 0:
        print("Number divisible by 5")
    else :
        print("Number not divisible by either")

divisibility(11)