class MultiDispatch(type):
    def __new__(cls, name, bases, namespace):
        new_class = super().__new__(cls, name, bases, namespace)
        dispatch_table = {}

        for attr_name, attr_value in namespace.items():
            if hasattr(attr_value, '__dispatch_types__'):
                if attr_name not in dispatch_table:
                    dispatch_table[attr_name] = {}
                dispatch_table[attr_name][attr_value.__dispatch_types__] = attr_value

        for attr_name, table in dispatch_table.items():
            def dispatcher(*args, **kwargs):
                arg_types = tuple(type(arg) for arg in args)
                if arg_types in table:
                    return table[arg_types](*args, **kwargs)
                else:
                    raise TypeError(f"No matching method for types {arg_types}")
            setattr(new_class, attr_name, dispatcher)
        
        return new_class

def dispatch(*types):
    def decorator(func):
        func.__dispatch_types__ = types
        return func
    return decorator

class MyClass(metaclass=MultiDispatch):
    @dispatch(int, int)
    def add(self, a, b):
        return a + b

    @dispatch(str, str)
    def add(self, a, b):
        return a + " " + b

    @dispatch(list, list)
    def add(self, a, b):
        return a + b

if __name__ == "__main__":
    obj = MyClass()
    print(obj.add(1, 2))
    print(obj.add("Hello", "World"))
    print(obj.add([1, 2], [3, 4]))

    try:
        obj.add(1, "World")
    except TypeError as e:
        print(f"Caught expected error: {e}")