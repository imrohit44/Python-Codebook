class EnumMeta(type):
    def __new__(cls, name, bases, namespace):
        members = {}
        for attr_name, attr_value in namespace.items():
            if not attr_name.startswith('_') and not callable(attr_value):
                members[attr_name] = attr_value

        namespace['_members'] = members
        
        def __iter__(self):
            return iter(self._members.keys())

        def __getitem__(self, key):
            return self._members.get(key)
        
        namespace['__iter__'] = __iter__
        namespace['__getitem__'] = __getitem__

        return super().__new__(cls, name, bases, namespace)
        
    def __setattr__(cls, name, value):
        if name not in cls.__dict__ and '_members' in cls.__dict__:
            raise TypeError("Cannot add new members to an enum.")
        super().__setattr__(name, value)
        
class Color(metaclass=EnumMeta):
    RED = 1
    GREEN = 2
    BLUE = 3

if __name__ == '__main__':
    print(Color.RED)
    
    for color in Color:
        print(f"Color: {color}, Value: {Color[color]}")
    
    try:
        Color.YELLOW = 4
    except TypeError as e:
        print(e)