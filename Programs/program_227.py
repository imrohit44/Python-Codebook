import inspect

def make_dataclass(name, fields):
    
    def __init__(self, **kwargs):
        for field, value in kwargs.items():
            setattr(self, field, value)
            
    namespace = {'__init__': __init__}
    
    new_class = type(name, (object,), namespace)
    
    new_class.__annotations__ = fields
    
    return new_class

if __name__ == '__main__':
    Person = make_dataclass('Person', {'name': str, 'age': int})
    
    person1 = Person(name="Alice", age=30)
    print(person1.name)
    print(person1.age)
    
    try:
        person2 = Person(name="Bob", age="35")
    except TypeError as e:
        print(e)