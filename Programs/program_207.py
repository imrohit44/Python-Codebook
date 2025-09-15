class AutoProperties(type):
    def __new__(cls, name, bases, namespace):
        new_class = super().__new__(cls, name, bases, namespace)
        
        if '_properties' in namespace:
            for prop_name in namespace['_properties']:
                private_name = f'_{prop_name}'
                
                def getter(self, prop_name=prop_name):
                    return getattr(self, f'_{prop_name}')
                    
                def setter(self, value, prop_name=prop_name):
                    setattr(self, f'_{prop_name}', value)
                
                setattr(new_class, prop_name, property(getter, setter))
                
        return new_class

class User(metaclass=AutoProperties):
    _properties = ['name', 'email']
    
    def __init__(self, name, email):
        self._name = name
        self._email = email

if __name__ == '__main__':
    user = User("Alice", "alice@example.com")
    print(user.name)
    user.name = "Bob"
    print(user.name)