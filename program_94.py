import functools
import time

def timing_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f"Method '{func.__name__}' took {end_time - start_time:.4f}s")
        return result
    return wrapper

class InjectionMeta(type):
    def __new__(cls, name, bases, namespace):
        for attr_name, attr_value in namespace.items():
            if callable(attr_value):
                original_method = attr_value
                namespace[attr_name] = timing_decorator(original_method)
        return super().__new__(cls, name, bases, namespace)

class MyService(metaclass=InjectionMeta):
    def do_work(self, task_id):
        time.sleep(0.5)
        return f"Work for {task_id} done"

if __name__ == '__main__':
    service = MyService()
    service.do_work(1)