import inspect

class ValidatingDescriptor:
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
    age = ValidatingDescriptor(int, lambda x: 0 <= x <= 120)
    name = ValidatingDescriptor(str, lambda x: len(x) > 0)

    def __init__(self, name, age):
        self.name = name
        self.age = age

class Employee(User):
    employee_id = ValidatingDescriptor(str, lambda x: x.startswith('EMP'))

    def __init__(self, name, age, employee_id):
        super().__init__(name, age)
        self.employee_id = employee_id

if __name__ == '__main__':
    user = User("Alice", 30)
    print(f"User: {user.name}, {user.age}")
    
    employee = Employee("Bob", 40, "EMP123")
    print(f"Employee: {employee.name}, {employee.age}, {employee.employee_id}")

    try:
        employee.employee_id = "12345"
    except ValueError as e:
        print(e)