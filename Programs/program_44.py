class ValidatingValue:
    def __init__(self, value_type, validator=None):
        self.value_type = value_type
        self.validator = validator
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name, None)

    def __set__(self, obj, value):
        if not isinstance(value, self.value_type):
            raise TypeError(f"Attribute '{self.name}' must be of type {self.value_type.__name__}.")
        if self.validator and not self.validator(value):
            raise ValueError(f"Value '{value}' for attribute '{self.name}' failed validation.")
        obj.__dict__[self.name] = value

class User:
    age = ValidatingValue(int, lambda x: 0 <= x <= 120)
    name = ValidatingValue(str, lambda x: len(x) > 0)

    def __init__(self, name, age):
        self.name = name
        self.age = age

if __name__ == "__main__":
    user1 = User("Alice", 30)
    print(f"Name: {user1.name}, Age: {user1.age}")

    try:
        user1.age = 200
    except ValueError as e:
        print(f"Caught expected error: {e}")

    try:
        user1.age = "thirty"
    except TypeError as e:
        print(f"Caught expected error: {e}")

    try:
        user2 = User("", 25)
    except ValueError as e:
        print(f"Caught expected error: {e}")