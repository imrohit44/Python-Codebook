import time
import random
from functools import wraps

def retry(retries=3, delay=1, backoff=2, exceptions=(Exception,)):
    """
    A decorator to retry a function if it raises a specified exception.

    Args:
        retries (int): Maximum number of retries.
        delay (int/float): Initial delay in seconds between retries.
        backoff (int/float): Factor by which the delay increases each time.
        exceptions (tuple): A tuple of exception types to catch and retry on.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            mtries = retries
            mdelay = delay
            while mtries > 0:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    mtries -= 1
                    if mtries > 0:
                        print(f"Retrying '{func.__name__}' in {mdelay:.2f} seconds due to: {e}")
                        time.sleep(mdelay)
                        mdelay *= backoff
                    else:
                        raise  # Re-raise the last exception if retries are exhausted
        return wrapper
    return decorator

# Example Usage:

call_count = 0

@retry(retries=5, delay=0.5, backoff=1.5, exceptions=(ValueError,))
def might_fail_value_error(x):
    global call_count
    call_count += 1
    print(f"Attempt {call_count} for might_fail_value_error({x})")
    if call_count < 3:
        raise ValueError("Simulating a temporary value error")
    return f"Success! Value is {x}"

@retry(retries=2, exceptions=(IOError, TypeError))
def might_fail_io_error():
    print("Attempting to simulate IO error")
    if random.random() < 0.8:
        raise IOError("Simulating a file system error")
    return "IO operation successful!"

# --- Test cases ---
print("--- Testing might_fail_value_error ---")
call_count = 0 # Reset for this test
try:
    result1 = might_fail_value_error(10)
    print(result1)
except ValueError as e:
    print(f"Failed after retries: {e}")

print("\n--- Testing might_fail_io_error ---")
try:
    result2 = might_fail_io_error()
    print(result2)
except (IOError, TypeError) as e:
    print(f"Failed after retries: {e}")

print("\n--- Testing a function that always succeeds ---")
@retry(retries=3)
def always_succeeds():
    print("This function always succeeds.")
    return "Always a win!"

print(always_succeeds())