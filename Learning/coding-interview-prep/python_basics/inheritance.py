# Inheritance lets one class "borrow" features from another class.
# The parent class has shared features; child classes add their own.
# This avoids repeating code and lets you build on existing work.

# --- Parent class ---
class Animal:
    def __init__(self, name, sound):
        self.name = name
        self.sound = sound

    def speak(self):
        print(f"{self.name} says {self.sound}!")

    def eat(self):
        print(f"{self.name} is eating.")

# --- Child class: inherits from Animal, adds its own features ---
class Dog(Animal):
    def __init__(self, name):
        super().__init__(name, "Woof")   # call parent's __init__ with Dog's sound
        self.tricks = []

    def fetch(self):
        print(f"{self.name} fetches the ball!")

class Cat(Animal):
    def __init__(self, name):
        super().__init__(name, "Meow")

    def purr(self):
        print(f"{self.name} is purring...")

# --- Multiple inheritance: inherit from more than one parent ---
class Flyable:
    def fly(self):
        print(f"{self.name} is flying!")

class FlyingDog(Dog, Flyable):
    pass   # inherits everything from both Dog and Flyable

if __name__ == "__main__":
    dog = Dog("Rex")
    cat = Cat("Whiskers")

    dog.speak()    # inherited from Animal
    dog.eat()      # inherited from Animal
    dog.fetch()    # unique to Dog

    cat.speak()
    cat.purr()

    flying_dog = FlyingDog("Superdog")
    flying_dog.speak()
    flying_dog.fetch()
    flying_dog.fly()   # from Flyable
