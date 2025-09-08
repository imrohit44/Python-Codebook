import time
import threading
from collections import deque
from functools import wraps

def rate_limit(calls_per_second: float):
    """
    A decorator that rate-limits the decorated function.
    Calls will block if the rate limit is exceeded.

    Args:
        calls_per_second (float): The maximum number of calls allowed per second.
    """
    if calls_per_second <= 0:
        raise ValueError("calls_per_second must be positive.")
    
    # Calculate the minimum time required between calls
    # If 10 calls/sec, then 0.1 sec/call minimum
    min_interval = 1.0 / calls_per_second

    # Use a deque to store timestamps of recent calls
    # This acts as a sliding window to track calls
    call_timestamps = deque()
    lock = threading.Lock() # Protect access to call_timestamps

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with lock:
                current_time = time.monotonic() # Use monotonic for reliable time differences

                # Remove timestamps of calls that are outside the current window
                # The window size is 1 second, so remove anything older than current_time - 1
                while call_timestamps and call_timestamps[0] <= current_time - 1.0:
                    call_timestamps.popleft()

                # If the number of calls in the last second is at or above the limit,
                # we need to wait.
                if len(call_timestamps) >= calls_per_second:
                    # Calculate how long to wait. It's the time until the oldest call in the window
                    # is older than 1 second from now, plus the min_interval for the next call.
                    wait_until = call_timestamps[0] + 1.0 # This is the time when the window opens up
                    sleep_duration = wait_until - current_time
                    
                    if sleep_duration > 0:
                        # print(f"Rate limited: Sleeping for {sleep_duration:.4f}s before calling {func.__name__}...")
                        time.sleep(sleep_duration)
                        current_time = time.monotonic() # Update current_time after sleeping

                # Add the new call's timestamp
                call_timestamps.append(current_time)
                
            return func(*args, **kwargs)
        return wrapper
    return decorator

# --- Example Usage ---

# Simulate a service that can only handle 2 calls per second
@rate_limit(calls_per_second=2)
def limited_service_call(call_id):
    current_time = time.monotonic()
    print(f"[{current_time:.4f}] Service Call {call_id}: Executing...")
    time.sleep(0.05) # Simulate quick work
    return f"Call {call_id} done."

def client_thread(thread_id):
    for i in range(5):
        try:
            result = limited_service_call(f"T{thread_id}-C{i+1}")
            # print(result) # Uncomment to see individual call results
        except Exception as e:
            print(f"Client {thread_id}: Error calling service: {e}")
        # time.sleep(0.1) # Clients might try to call rapidly

if __name__ == "__main__":
    print("Starting rate limiting demonstration (2 calls/second limit)...")
    start_time = time.monotonic()

    threads = []
    num_threads = 3 # Multiple clients trying to hit the service
    for i in range(num_threads):
        thread = threading.Thread(target=client_thread, args=(i+1,))
        threads.append(thread)
        thread.start()

    for t in threads:
        t.join()

    end_time = time.monotonic()
    print(f"\nAll calls completed in {end_time - start_time:.4f} seconds.")
    print("Observe the timestamps to see the rate limiting in action.")