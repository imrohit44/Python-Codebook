import inspect

def type_check(func):
    sig = inspect.signature(func)
    
    def wrapper(*args, **kwargs):
        bound_args = sig.bind(*args, **kwargs)
        for name, value in bound_args.arguments.items():
            param_type = sig.parameters[name].annotation
            if param_type is not inspect.Parameter.empty and not isinstance(value, param_type):
                raise TypeError(f"Argument '{name}' must be of type {param_type.__name__}, got {type(value).__name__}")
        
        result = func(*args, **kwargs)
        
        return_type = sig.return_annotation
        if return_type is not inspect.Parameter.empty and not isinstance(result, return_type):
            raise TypeError(f"Return value must be of type {return_type.__name__}, got {type(result).__name__}")
            
        return result

    return wrapper

@type_check
def add_numbers(a: int, b: int) -> int:
    return a + b

@type_check
def greet(name: str) -> str:
    return f"Hello, {name}"

if __name__ == '__main__':
    print(add_numbers(1, 2))
    print(greet("Alice"))
    
    try:
        add_numbers(1, "2")
    except TypeError as e:
        print(e)