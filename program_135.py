def dispatch(*types):
    def decorator(func):
        func.__dispatch_types__ = types
        return func
    return decorator

class MultiDispatch(type):
    def __new__(cls, name, bases, namespace):
        dispatch_table = {}

        for attr_name, attr_value in namespace.items():
            if hasattr(attr_value, '__dispatch_types__'):
                if attr_name not in dispatch_table:
                    dispatch_table[attr_name] = {}
                dispatch_table[attr_name][attr_value.__dispatch_types__] = attr_value

        for attr_name, table in dispatch_table.items():
            def dispatcher(*args, **kwargs):
                arg_types = tuple(type(arg) for arg in args[1:])
                if arg_types in table:
                    return table[arg_types](*args, **kwargs)
                else:
                    raise TypeError(f"No matching method for types {arg_types}")
            namespace[attr_name] = dispatcher
        
        return super().__new__(cls, name, bases, namespace)

class Calculator(metaclass=MultiDispatch):
    @dispatch(int, int)
    def add(self, a, b):
        return a + b

    @dispatch(str, str)
    def add(self, a, b):
        return a + " " + b

if __name__ == '__main__':
    calc = Calculator()
    print(calc.add(1, 2))
    print(calc.add("Hello", "World"))
    try:
        calc.add(1, "World")
    except TypeError as e:
        print(e)