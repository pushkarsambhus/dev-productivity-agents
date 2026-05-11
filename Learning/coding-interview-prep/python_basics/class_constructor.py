# __init__ is the "constructor" — it runs automatically when you create an object.
# Instance variables belong to each specific object.
# Class variables are shared by ALL objects of that class.
# __str__ controls what you see when you print an object.
# __repr__ is a developer-friendly representation of the object.

class Car:
    # Class variable: shared by ALL Car objects
    total_cars_made = 0

    def __init__(self, make, model, year):
        # Instance variables: unique to each Car object
        self.make = make
        self.model = model
        self.year = year
        self.is_running = False          # all cars start turned off

        Car.total_cars_made += 1         # update the shared counter

    def start(self):
        self.is_running = True
        print(f"{self.make} {self.model} is now running.")

    def stop(self):
        self.is_running = False
        print(f"{self.make} {self.model} has stopped.")

    def __str__(self):
        # This is what gets printed when you use print(car)
        return f"{self.year} {self.make} {self.model}"

    def __repr__(self):
        # This is a detailed representation useful for debugging
        return f"Car(make='{self.make}', model='{self.model}', year={self.year})"

if __name__ == "__main__":
    car1 = Car("Toyota", "Camry", 2022)
    car2 = Car("Honda", "Civic", 2021)

    print("Car 1:", car1)              # uses __str__
    print("Car 2:", car2)
    print("Repr:", repr(car1))         # uses __repr__
    print("Total cars made:", Car.total_cars_made)

    car1.start()
    car1.stop()
