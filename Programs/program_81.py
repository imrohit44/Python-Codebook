import functools

def timing_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f"Method '{func.__name__}' took {end_time - start_time:.4f}s")
        return result
    return wrapper

def logging_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling method '{func.__name__}'")
        result = func(*args, **kwargs)
        print(f"Method '{func.__name__}' returned {result}")
        return result
    return wrapper

class InjectionMeta(type):
    def __new__(cls, name, bases, namespace):
        decorators = [logging_decorator, timing_decorator]
        
        for attr_name, attr_value in namespace.items():
            if callable(attr_value) and hasattr(attr_value, '__inject_flag__'):
                original_method = attr_value
                for dec in reversed(decorators):
                    original_method = dec(original_method)
                namespace[attr_name] = original_method
                
        return super().__new__(cls, name, bases, namespace)

def inject(func):
    func.__inject_flag__ = True
    return func

class MyService(metaclass=InjectionMeta):
    @inject
    def do_work(self, task_id):
        time.sleep(0.5)
        return f"Work for {task_id} done"

    def do_nothing(self):
        print("This method is not injected.")

if __name__ == '__main__':
    service = MyService()
    service.do_work(1)
    service.do_nothing()