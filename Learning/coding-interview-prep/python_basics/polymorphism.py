# Polymorphism means "many forms" — the same action works differently depending on the object.
# For example, all shapes have an "area", but the formula differs per shape.
# Duck typing: Python doesn't care what TYPE an object is, only that it has the right methods.

class Shape:
    def area(self):
        return 0   # base version, meant to be overridden

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        # Override the parent's area() with Circle-specific logic
        return 3.14159 * self.radius ** 2

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

class Triangle(Shape):
    def __init__(self, base, height):
        self.base = base
        self.height = height

    def area(self):
        return 0.5 * self.base * self.height

# --- Duck typing: works with any object that has a .speak() method ---
class Duck:
    def speak(self):
        return "Quack!"

class Person:
    def speak(self):
        return "Hello!"

def make_it_speak(thing):
    # We don't check IF it's a Duck or Person — we just call speak()
    print(thing.speak())

if __name__ == "__main__":
    shapes = [Circle(5), Rectangle(4, 6), Triangle(3, 8)]

    for shape in shapes:
        # same call — area() — different result for each shape
        print(f"{shape.__class__.__name__} area: {shape.area():.2f}")

    print("\nDuck typing:")
    make_it_speak(Duck())
    make_it_speak(Person())
