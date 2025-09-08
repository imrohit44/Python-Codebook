import functools
import time

# --- 1. The Aspect Decorator ---
def add_aspect(before=None, after=None):
    """
    Decorator to mark a method for aspect weaving and define its before/after hooks.
    
    Args:
        before (callable, optional): A function to execute before the decorated method.
                                     Signature: `before(instance, method_name, *args, **kwargs)`
        after (callable, optional): A function to execute after the decorated method.
                                    Signature: `after(instance, method_name, result, *args, **kwargs)`
    """
    def decorator(func):
        # Store the aspect hooks directly on the function object
        func._aspect_before = before
        func._aspect_after = after
        func._is_aspect_weavable = True # Mark this method for weaving
        return func
    return decorator

# --- Example Aspect Functions ---
def log_before(instance, method_name, *args, **kwargs):
    print(f"[BeforeAspect] Calling '{method_name}' on {instance.__class__.__name__} with args={args}, kwargs={kwargs}")

def log_after(instance, method_name, result, *args, **kwargs):
    print(f"[AfterAspect] '{method_name}' on {instance.__class__.__name__} returned: {result}")

def time_method_before(instance, method_name, *args, **kwargs):
    instance._aspect_start_time = time.perf_counter() # Store start time on instance

def time_method_after(instance, method_name, result, *args, **kwargs):
    end_time = time.perf_counter()
    duration = end_time - instance._aspect_start_time
    print(f"[TimeAspect] '{method_name}' on {instance.__class__.__name__} took {duration:.4f}s")


# --- 2. The Aspect Weaver ---
class AspectWeaver:
    """
    Dynamically weaves aspects into methods of a target instance.
    """
    @staticmethod
    def weave(target_instance: object):
        """
        Replaces decorated methods in `target_instance` with proxied versions
        that include the before/after aspects.
        """
        print(f"\nWeaving aspects into instance of {target_instance.__class__.__name__}...")
        
        # Iterate over the original class's dictionary to find methods marked for weaving
        for name, method_obj in target_instance.__class__.__dict__.items():
            if callable(method_obj) and hasattr(method_obj, '_is_aspect_weavable') and method_obj._is_aspect_weavable:
                original_method = getattr(target_instance, name) # Get the bound method from the instance
                
                before_hook = method_obj._aspect_before
                after_hook = method_obj._aspect_after

                print(f"  Weaving aspect into method: {name}")

                @functools.wraps(original_method) # Preserve metadata like __name__, __doc__
                def proxied_method(*args, **kwargs):
                    if before_hook:
                        before_hook(target_instance, name, *args, **kwargs)
                    
                    result = original_method(*args, **kwargs) # Call the original method
                    
                    if after_hook:
                        after_hook(target_instance, name, result, *args, **kwargs)
                    
                    return result
                
                # Replace the original method on the *instance* with the new proxied method
                setattr(target_instance, name, proxied_method)
        
        print("Aspect weaving complete.")
        return target_instance # Return the modified instance

# --- Example Usage ---

# Define a sample class with methods to be advised
class MyService:
    def __init__(self, name):
        self.name = name
        print(f"MyService '{self.name}' created.")

    @add_aspect(before=log_before, after=log_after)
    def do_work(self, task_id: int, data: str):
        print(f"  [{self.name}]: Performing work for task {task_id} with data '{data}'")
        return f"Work done for {task_id}"

    @add_aspect(before=log_before, after=log_after)
    @add_aspect(before=time_method_before, after=time_method_after) # Multiple aspects can be stacked
    def calculate_something(self, value_a: float, value_b: float):
        print(f"  [{self.name}]: Calculating {value_a} * {value_b}...")
        time.sleep(0.1) # Simulate some calculation time
        result = value_a * value_b
        print(f"  [{self.name}]: Calculation result: {result}")
        return result

    def non_weaved_method(self):
        print(f"  [{self.name}]: This method is not weaved.")
        return "Not Weaved"

if __name__ == "__main__":
    service_instance = MyService("ServiceA")
    another_service_instance = MyService("ServiceB")

    print("\n--- Calling methods BEFORE weaving ---")
    service_instance.do_work(1, "initial data")
    service_instance.calculate_something(10, 5)
    service_instance.non_weaved_method()

    # Weave aspects into service_instance
    weaved_service = AspectWeaver.weave(service_instance)

    print("\n--- Calling methods AFTER weaving on 'weaved_service' ---")
    weaved_service.do_work(2, "processed data")
    weaved_service.calculate_something(7, 3)
    weaved_service.non_weaved_method() # This method should still be original

    print("\n--- Calling methods on 'another_service_instance' (should remain unweaved) ---")
    another_service_instance.do_work(3, "raw data")
    another_service_instance.calculate_something(20, 2)