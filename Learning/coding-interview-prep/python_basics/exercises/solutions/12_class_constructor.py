# SOLUTIONS: Class Constructors and Special Methods
# These are reference solutions — there are often multiple valid ways to solve each problem!

import math

# ===========================================================================
# Problem 1 Solution: __str__ and __repr__ Methods
# ===========================================================================

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"Person: {self.name} ({self.age})"

    def __repr__(self):
        return f"Person('{self.name}', {self.age})"

person = Person("Alice", 30)
print(str(person))
print(repr(person))


# ===========================================================================
# Problem 2 Solution: Class Variable - Population Counter
# ===========================================================================

class Person:
    population = 0

    def __init__(self, name, age):
        self.name = name
        self.age = age
        Person.population += 1

    def __str__(self):
        return f"Person: {self.name} ({self.age})"

    def __repr__(self):
        return f"Person('{self.name}', {self.age})"

p1 = Person("Alice", 30)
print(Person.population)
p2 = Person("Bob", 25)
print(Person.population)
p3 = Person("Carol", 35)
print(Person.population)


# ===========================================================================
# Problem 3 Solution: Temperature Class with Properties
# ===========================================================================

class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    @property
    def fahrenheit(self):
        return (self.celsius * 9/5) + 32

    @property
    def kelvin(self):
        return self.celsius + 273.15

temp = Temperature(0)
print(temp.fahrenheit)
print(temp.kelvin)


# ===========================================================================
# Problem 4 Solution: Temperature Equality
# ===========================================================================

class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    @property
    def fahrenheit(self):
        return (self.celsius * 9/5) + 32

    @property
    def kelvin(self):
        return self.celsius + 273.15

    def __eq__(self, other):
        return self.celsius == other.celsius

temp1 = Temperature(0)
temp2 = Temperature(0)
temp3 = Temperature(10)
print(temp1 == temp2)
print(temp1 == temp3)


# ===========================================================================
# Problem 5 Solution: Vector2D Class
# ===========================================================================

class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return f"Vector2D({self.x}, {self.y})"

    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

vec = Vector2D(3, 4)
print(str(vec))
print(repr(vec))
print(vec.magnitude())


if __name__ == "__main__":
    print("=== Running all solutions ===")

    print("\nProblem 1:")
    class Person:
        def __init__(self, name, age):
            self.name = name
            self.age = age

        def __str__(self):
            return f"Person: {self.name} ({self.age})"

        def __repr__(self):
            return f"Person('{self.name}', {self.age})"

    person = Person("Alice", 30)
    print(str(person))
    print(repr(person))

    print("\nProblem 2:")
    class Person:
        population = 0

        def __init__(self, name, age):
            self.name = name
            self.age = age
            Person.population += 1

        def __str__(self):
            return f"Person: {self.name} ({self.age})"

        def __repr__(self):
            return f"Person('{self.name}', {self.age})"

    p1 = Person("Alice", 30)
    print(Person.population)
    p2 = Person("Bob", 25)
    print(Person.population)
    p3 = Person("Carol", 35)
    print(Person.population)

    print("\nProblem 3:")
    class Temperature:
        def __init__(self, celsius):
            self.celsius = celsius

        @property
        def fahrenheit(self):
            return (self.celsius * 9/5) + 32

        @property
        def kelvin(self):
            return self.celsius + 273.15

    temp = Temperature(0)
    print(temp.fahrenheit)
    print(temp.kelvin)

    print("\nProblem 4:")
    class Temperature:
        def __init__(self, celsius):
            self.celsius = celsius

        @property
        def fahrenheit(self):
            return (self.celsius * 9/5) + 32

        @property
        def kelvin(self):
            return self.celsius + 273.15

        def __eq__(self, other):
            return self.celsius == other.celsius

    temp1 = Temperature(0)
    temp2 = Temperature(0)
    temp3 = Temperature(10)
    print(temp1 == temp2)
    print(temp1 == temp3)

    print("\nProblem 5:")
    class Vector2D:
        def __init__(self, x, y):
            self.x = x
            self.y = y

        def __str__(self):
            return f"({self.x}, {self.y})"

        def __repr__(self):
            return f"Vector2D({self.x}, {self.y})"

        def magnitude(self):
            return math.sqrt(self.x ** 2 + self.y ** 2)

    vec = Vector2D(3, 4)
    print(str(vec))
    print(repr(vec))
    print(vec.magnitude())
