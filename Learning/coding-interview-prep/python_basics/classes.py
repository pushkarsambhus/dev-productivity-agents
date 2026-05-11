# A class is like a blueprint for creating objects.
# For example, a "Dog" class describes what every dog has (name, breed)
# and what every dog can do (bark, fetch).

class Dog:
    # 'self' refers to the specific dog object being created or used
    # Think of 'self' as "this particular dog"

    def __init__(self, name, breed):
        # This method runs automatically when you create a new Dog
        self.name = name          # store the name on this dog
        self.breed = breed        # store the breed on this dog
        self.tricks = []          # each dog starts with an empty list of tricks

    def bark(self):
        # A method is a function that belongs to the class
        print(f"{self.name} says: Woof!")

    def learn_trick(self, trick):
        self.tricks.append(trick)   # add the trick to this dog's list
        print(f"{self.name} learned: {trick}")

    def show_tricks(self):
        if self.tricks:
            print(f"{self.name}'s tricks: {', '.join(self.tricks)}")
        else:
            print(f"{self.name} doesn't know any tricks yet.")

if __name__ == "__main__":
    # Create two separate Dog objects from the same blueprint
    dog1 = Dog("Rex", "German Shepherd")
    dog2 = Dog("Bella", "Poodle")

    dog1.bark()
    dog2.bark()

    dog1.learn_trick("sit")
    dog1.learn_trick("shake")
    dog2.learn_trick("roll over")

    dog1.show_tricks()
    dog2.show_tricks()
