class custom_property:
    def __init__(self, getter):
        self.getter = getter
        self.setter = None
        self.deleter = None
    
    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = '_' + name
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        if self.setter is None:
            raise AttributeError("can't set attribute")
        self.setter(obj, value)

    def __delete__(self, obj):
        if self.deleter is None:
            raise AttributeError("can't delete attribute")
        self.deleter(obj)

    def setter(self, func):
        self.setter = func
        return self

    def deleter(self, func):
        self.deleter = func
        return self

class Temperature:
    def __init__(self, value=0.0):
        self._celsius = value

    @custom_property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Temperature below absolute zero is not possible.")
        self._celsius = value

    @celsius.deleter
    def celsius(self,):
        del self._celsius

if __name__ == "__main__":
    t = Temperature(25)
    print(t.celsius)
    t.celsius = 30
    print(t.celsius)
    
    try:
        t.celsius = -300
    except ValueError as e:
        print(e)
    
    del t.celsius
    try:
        print(t.celsius)
    except AttributeError as e:
        print(e)