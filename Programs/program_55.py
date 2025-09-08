import inspect

class DataValidator(type):
    def __new__(cls, name, bases, namespace):
        new_class = super().__new__(cls, name, bases, namespace)
        for attr_name, attr_value in namespace.items():
            if inspect.isfunction(attr_value) and attr_name.startswith('_validate_'):
                field_name = attr_name[len('_validate_'):]
                
                def setter(self, value):
                    attr_value(self, value)
                    super(new_class, self).__setattr__(field_name, value)
                
                setattr(new_class, f'set_{field_name}', setter)
                
        return new_class

class User(metaclass=DataValidator):
    def __init__(self, name, email):
        self.set_name(name)
        self.set_email(email)
    
    def _validate_name(self, value):
        if not isinstance(value, str) or len(value) < 1:
            raise ValueError("Name must be a non-empty string.")
            
    def _validate_email(self, value):
        if "@" not in value:
            raise ValueError("Invalid email address.")

if __name__ == "__main__":
    user = User("Alice", "alice@example.com")
    print(f"User created: {user.name}, {user.email}")
    
    try:
        user.set_name("")
    except ValueError as e:
        print(f"Caught expected error: {e}")
        
    try:
        user.set_email("invalid-email")
    except ValueError as e:
        print(f"Caught expected error: {e}")