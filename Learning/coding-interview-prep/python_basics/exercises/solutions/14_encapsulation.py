# SOLUTIONS: Encapsulation
# These are reference solutions — there are often multiple valid ways to solve each problem!

# ===========================================================================
# Problem 1 Solution: Public, Protected, and Private Attributes
# ===========================================================================

class Person:
    def __init__(self, name, email, ssn):
        self.name = name  # public
        self._email = email  # protected
        self.__ssn = ssn  # private

person = Person("Alice", "alice@example.com", "123-45-6789")
print(person.name)
print(person._email)
# Private attributes are name-mangled: _ClassName__attributeName
print("_Person__ssn" in dir(person))


# ===========================================================================
# Problem 2 Solution: Email Property with Validation
# ===========================================================================

class Person:
    def __init__(self, name, email, ssn):
        self.name = name
        self._email = email
        self.__ssn = ssn

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if "@" not in value:
            raise ValueError("Invalid email format")
        self._email = value

person = Person("Alice", "alice@example.com", "123-45-6789")
print(person.email)

try:
    person.email = "invalid-email"
except ValueError as e:
    print(e)


# ===========================================================================
# Problem 3 Solution: TemperatureSensor with Private Celsius
# ===========================================================================

class TemperatureSensor:
    def __init__(self, celsius):
        self.__celsius = celsius

    @property
    def temperature(self):
        return self.__celsius

    @temperature.setter
    def temperature(self, value):
        if value < -273.15:
            raise ValueError("Temperature cannot be below -273.15")
        self.__celsius = value

sensor = TemperatureSensor(20)
print(sensor.temperature)

try:
    sensor.temperature = -300
except ValueError as e:
    print(e)


# ===========================================================================
# Problem 4 Solution: Temperature Status Property
# ===========================================================================

class TemperatureSensor:
    def __init__(self, celsius):
        self.__celsius = celsius

    @property
    def temperature(self):
        return self.__celsius

    @temperature.setter
    def temperature(self, value):
        if value < -273.15:
            raise ValueError("Temperature cannot be below -273.15")
        self.__celsius = value

    @property
    def status(self):
        if self.__celsius < 0:
            return "freezing"
        elif self.__celsius <= 15:
            return "cold"
        elif self.__celsius <= 25:
            return "warm"
        else:
            return "hot"

sensor1 = TemperatureSensor(-5)
print(sensor1.status)

sensor2 = TemperatureSensor(10)
print(sensor2.status)

sensor3 = TemperatureSensor(20)
print(sensor3.status)

sensor4 = TemperatureSensor(30)
print(sensor4.status)


# ===========================================================================
# Problem 5 Solution: Counter with Private Count
# ===========================================================================

class Counter:
    def __init__(self):
        self.__count = 0

    def increment(self):
        self.__count += 1

    def decrement(self):
        if self.__count > 0:
            self.__count -= 1

    def reset(self):
        self.__count = 0

    @property
    def count(self):
        return self.__count

counter = Counter()
counter.increment()
print(counter.count)

counter.decrement()
print(counter.count)

try:
    counter.count = 5
except AttributeError as e:
    print(f"Cannot set attribute")


if __name__ == "__main__":
    print("=== Running all solutions ===")

    print("\nProblem 1:")
    class Person:
        def __init__(self, name, email, ssn):
            self.name = name
            self._email = email
            self.__ssn = ssn

    person = Person("Alice", "alice@example.com", "123-45-6789")
    print(person.name)
    print(person._email)
    print("_Person__ssn" in dir(person))

    print("\nProblem 2:")
    class Person:
        def __init__(self, name, email, ssn):
            self.name = name
            self._email = email
            self.__ssn = ssn

        @property
        def email(self):
            return self._email

        @email.setter
        def email(self, value):
            if "@" not in value:
                raise ValueError("Invalid email format")
            self._email = value

    person = Person("Alice", "alice@example.com", "123-45-6789")
    print(person.email)
    try:
        person.email = "invalid-email"
    except ValueError as e:
        print(e)

    print("\nProblem 3:")
    class TemperatureSensor:
        def __init__(self, celsius):
            self.__celsius = celsius

        @property
        def temperature(self):
            return self.__celsius

        @temperature.setter
        def temperature(self, value):
            if value < -273.15:
                raise ValueError("Temperature cannot be below -273.15")
            self.__celsius = value

    sensor = TemperatureSensor(20)
    print(sensor.temperature)
    try:
        sensor.temperature = -300
    except ValueError as e:
        print(e)

    print("\nProblem 4:")
    class TemperatureSensor:
        def __init__(self, celsius):
            self.__celsius = celsius

        @property
        def temperature(self):
            return self.__celsius

        @temperature.setter
        def temperature(self, value):
            if value < -273.15:
                raise ValueError("Temperature cannot be below -273.15")
            self.__celsius = value

        @property
        def status(self):
            if self.__celsius < 0:
                return "freezing"
            elif self.__celsius <= 15:
                return "cold"
            elif self.__celsius <= 25:
                return "warm"
            else:
                return "hot"

    sensor1 = TemperatureSensor(-5)
    print(sensor1.status)
    sensor2 = TemperatureSensor(10)
    print(sensor2.status)
    sensor3 = TemperatureSensor(20)
    print(sensor3.status)
    sensor4 = TemperatureSensor(30)
    print(sensor4.status)

    print("\nProblem 5:")
    class Counter:
        def __init__(self):
            self.__count = 0

        def increment(self):
            self.__count += 1

        def decrement(self):
            if self.__count > 0:
                self.__count -= 1

        def reset(self):
            self.__count = 0

        @property
        def count(self):
            return self.__count

    counter = Counter()
    counter.increment()
    print(counter.count)
    counter.decrement()
    print(counter.count)
    try:
        counter.count = 5
    except AttributeError as e:
        print(f"Cannot set attribute")
