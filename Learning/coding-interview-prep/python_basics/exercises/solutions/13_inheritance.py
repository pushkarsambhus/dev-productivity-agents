# SOLUTIONS: Inheritance
# These are reference solutions — there are often multiple valid ways to solve each problem!

# ===========================================================================
# Problem 1 Solution: Vehicle Base Class
# ===========================================================================

class Vehicle:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year

    def description(self):
        return f"{self.year} {self.make} {self.model}"

class Car(Vehicle):
    def __init__(self, make, model, year, num_doors):
        super().__init__(make, model, year)
        self.num_doors = num_doors

class Motorcycle(Vehicle):
    def __init__(self, make, model, year, has_sidecar):
        super().__init__(make, model, year)
        self.has_sidecar = has_sidecar

car = Car("Toyota", "Camry", 2020, 4)
print(car.description())

moto = Motorcycle("Harley-Davidson", "Street 750", 2019, False)
print(moto.description())


# ===========================================================================
# Problem 2 Solution: Override description() Method
# ===========================================================================

class Vehicle:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year

    def description(self):
        return f"{self.year} {self.make} {self.model}"

class Car(Vehicle):
    def __init__(self, make, model, year, num_doors):
        super().__init__(make, model, year)
        self.num_doors = num_doors

    def description(self):
        return f"{self.year} {self.make} {self.model} ({self.num_doors} doors)"

class Motorcycle(Vehicle):
    def __init__(self, make, model, year, has_sidecar):
        super().__init__(make, model, year)
        self.has_sidecar = has_sidecar

    def description(self):
        sidecar_text = "with sidecar" if self.has_sidecar else "no sidecar"
        return f"{self.year} {self.make} {self.model} ({sidecar_text})"

car = Car("Toyota", "Camry", 2020, 4)
print(car.description())

moto = Motorcycle("Harley-Davidson", "Street 750", 2019, False)
print(moto.description())


# ===========================================================================
# Problem 3 Solution: Use super() in Car
# ===========================================================================

class Vehicle:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year

    def description(self):
        return f"{self.year} {self.make} {self.model}"

class Car(Vehicle):
    def __init__(self, make, model, year, num_doors):
        super().__init__(make, model, year)
        self.num_doors = num_doors

    def description(self):
        return f"{self.year} {self.make} {self.model} ({self.num_doors} doors)"

car = Car("Toyota", "Camry", 2020, 4)
print(car.description())


# ===========================================================================
# Problem 4 Solution: Multiple Inheritance - Flyable Mixin
# ===========================================================================

class Vehicle:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year

    def description(self):
        return f"{self.year} {self.make} {self.model}"

class Car(Vehicle):
    def __init__(self, make, model, year, num_doors):
        super().__init__(make, model, year)
        self.num_doors = num_doors

    def description(self):
        return f"{self.year} {self.make} {self.model} ({self.num_doors} doors)"

class Flyable:
    def fly(self):
        return "Flying through the sky..."

class FlyingCar(Car, Flyable):
    pass

flying_car = FlyingCar("Toyota", "Camry", 2020, 4)
print(flying_car.description())
print(flying_car.fly())


# ===========================================================================
# Problem 5 Solution: Polymorphism with Mixed Objects
# ===========================================================================

class Vehicle:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year

    def description(self):
        return f"{self.year} {self.make} {self.model}"

class Car(Vehicle):
    def __init__(self, make, model, year, num_doors):
        super().__init__(make, model, year)
        self.num_doors = num_doors

    def description(self):
        return f"{self.year} {self.make} {self.model} ({self.num_doors} doors)"

class Motorcycle(Vehicle):
    def __init__(self, make, model, year, has_sidecar):
        super().__init__(make, model, year)
        self.has_sidecar = has_sidecar

    def description(self):
        sidecar_text = "with sidecar" if self.has_sidecar else "no sidecar"
        return f"{self.year} {self.make} {self.model} ({sidecar_text})"

class Flyable:
    def fly(self):
        return "Flying through the sky..."

class FlyingCar(Car, Flyable):
    pass

vehicles = [
    Car("Toyota", "Camry", 2020, 4),
    Motorcycle("Harley-Davidson", "Street 750", 2019, False),
    FlyingCar("Tesla", "Model 3", 2021, 2)
]

for vehicle in vehicles:
    print(vehicle.description())

flying_car = vehicles[2]
print(flying_car.fly())


if __name__ == "__main__":
    print("=== Running all solutions ===")

    print("\nProblem 1:")
    class Vehicle:
        def __init__(self, make, model, year):
            self.make = make
            self.model = model
            self.year = year

        def description(self):
            return f"{self.year} {self.make} {self.model}"

    class Car(Vehicle):
        def __init__(self, make, model, year, num_doors):
            super().__init__(make, model, year)
            self.num_doors = num_doors

    class Motorcycle(Vehicle):
        def __init__(self, make, model, year, has_sidecar):
            super().__init__(make, model, year)
            self.has_sidecar = has_sidecar

    car = Car("Toyota", "Camry", 2020, 4)
    print(car.description())
    moto = Motorcycle("Harley-Davidson", "Street 750", 2019, False)
    print(moto.description())

    print("\nProblem 2:")
    class Vehicle:
        def __init__(self, make, model, year):
            self.make = make
            self.model = model
            self.year = year

        def description(self):
            return f"{self.year} {self.make} {self.model}"

    class Car(Vehicle):
        def __init__(self, make, model, year, num_doors):
            super().__init__(make, model, year)
            self.num_doors = num_doors

        def description(self):
            return f"{self.year} {self.make} {self.model} ({self.num_doors} doors)"

    class Motorcycle(Vehicle):
        def __init__(self, make, model, year, has_sidecar):
            super().__init__(make, model, year)
            self.has_sidecar = has_sidecar

        def description(self):
            sidecar_text = "with sidecar" if self.has_sidecar else "no sidecar"
            return f"{self.year} {self.make} {self.model} ({sidecar_text})"

    car = Car("Toyota", "Camry", 2020, 4)
    print(car.description())
    moto = Motorcycle("Harley-Davidson", "Street 750", 2019, False)
    print(moto.description())

    print("\nProblem 3:")
    class Vehicle:
        def __init__(self, make, model, year):
            self.make = make
            self.model = model
            self.year = year

        def description(self):
            return f"{self.year} {self.make} {self.model}"

    class Car(Vehicle):
        def __init__(self, make, model, year, num_doors):
            super().__init__(make, model, year)
            self.num_doors = num_doors

        def description(self):
            return f"{self.year} {self.make} {self.model} ({self.num_doors} doors)"

    car = Car("Toyota", "Camry", 2020, 4)
    print(car.description())

    print("\nProblem 4:")
    class Vehicle:
        def __init__(self, make, model, year):
            self.make = make
            self.model = model
            self.year = year

        def description(self):
            return f"{self.year} {self.make} {self.model}"

    class Car(Vehicle):
        def __init__(self, make, model, year, num_doors):
            super().__init__(make, model, year)
            self.num_doors = num_doors

        def description(self):
            return f"{self.year} {self.make} {self.model} ({self.num_doors} doors)"

    class Flyable:
        def fly(self):
            return "Flying through the sky..."

    class FlyingCar(Car, Flyable):
        pass

    flying_car = FlyingCar("Toyota", "Camry", 2020, 4)
    print(flying_car.description())
    print(flying_car.fly())

    print("\nProblem 5:")
    class Vehicle:
        def __init__(self, make, model, year):
            self.make = make
            self.model = model
            self.year = year

        def description(self):
            return f"{self.year} {self.make} {self.model}"

    class Car(Vehicle):
        def __init__(self, make, model, year, num_doors):
            super().__init__(make, model, year)
            self.num_doors = num_doors

        def description(self):
            return f"{self.year} {self.make} {self.model} ({self.num_doors} doors)"

    class Motorcycle(Vehicle):
        def __init__(self, make, model, year, has_sidecar):
            super().__init__(make, model, year)
            self.has_sidecar = has_sidecar

        def description(self):
            sidecar_text = "with sidecar" if self.has_sidecar else "no sidecar"
            return f"{self.year} {self.make} {self.model} ({sidecar_text})"

    class Flyable:
        def fly(self):
            return "Flying through the sky..."

    class FlyingCar(Car, Flyable):
        pass

    vehicles = [
        Car("Toyota", "Camry", 2020, 4),
        Motorcycle("Harley-Davidson", "Street 750", 2019, False),
        FlyingCar("Tesla", "Model 3", 2021, 2)
    ]

    for vehicle in vehicles:
        print(vehicle.description())

    flying_car = vehicles[2]
    print(flying_car.fly())
