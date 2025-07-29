import time
import threading
from enum import Enum

# Define Circuit Breaker States
class CircuitBreakerState(Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF-OPEN"

class CircuitBreakerError(Exception):
    """Custom exception raised when the circuit is open."""
    pass

class CircuitBreaker:
    def __init__(self,
                 failure_threshold: int = 3,
                 reset_timeout_seconds: int = 5,
                 half_open_test_attempts: int = 1):
        
        self.failure_threshold = failure_threshold
        self.reset_timeout_seconds = reset_timeout_seconds
        self.half_open_test_attempts = half_open_test_attempts

        self._state = CircuitBreakerState.CLOSED
        self._failures = 0
        self._last_failure_time = None
        self._half_open_attempts_made = 0
        self._lock = threading.Lock() # For thread-safe state management

        print(f"Circuit Breaker initialized: Threshold={failure_threshold}, Reset Timeout={reset_timeout_seconds}s")

    def __call__(self, func):
        """
        Decorator that wraps the target function.
        """
        def wrapper(*args, **kwargs):
            with self._lock:
                current_state = self._state
                
                if current_state == CircuitBreakerState.OPEN:
                    if time.time() - self._last_failure_time > self.reset_timeout_seconds:
                        self._transition_to(CircuitBreakerState.HALF_OPEN)
                        print("Circuit Breaker: Transitioned to HALF-OPEN (timeout reached).")
                    else:
                        raise CircuitBreakerError("Circuit Breaker is OPEN. Not attempting operation.")
                
                if current_state == CircuitBreakerState.HALF_OPEN:
                    self._half_open_attempts_made += 1
                    if self._half_open_attempts_made > self.half_open_test_attempts:
                        # Too many attempts in half-open, go back to open
                        self._transition_to(CircuitBreakerState.OPEN)
                        print("Circuit Breaker: Half-open attempts exceeded, back to OPEN.")
                        raise CircuitBreakerError("Circuit Breaker in HALF-OPEN state, too many failures.")
                    
                    # Allow one request to pass through for testing
                    print(f"Circuit Breaker: In HALF-OPEN state. Allowing test attempt {self._half_open_attempts_made}...")
            
            try:
                result = func(*args, **kwargs)
                with self._lock:
                    self._on_success()
                return result
            except Exception as e:
                with self._lock:
                    self._on_failure()
                raise e # Re-raise the original exception

        return wrapper

    def _transition_to(self, new_state: CircuitBreakerState):
        """Internal method to change the state and reset counters."""
        self._state = new_state
        if new_state == CircuitBreakerState.CLOSED:
            self._failures = 0
            self._last_failure_time = None
            self._half_open_attempts_made = 0
            print("Circuit Breaker: State -> CLOSED")
        elif new_state == CircuitBreakerState.OPEN:
            self._last_failure_time = time.time()
            print("Circuit Breaker: State -> OPEN")
        elif new_state == CircuitBreakerState.HALF_OPEN:
            self._half_open_attempts_made = 0 # Reset attempts for this half-open period
            print("Circuit Breaker: State -> HALF-OPEN")

    def _on_success(self):
        """Called when the wrapped function succeeds."""
        if self._state == CircuitBreakerState.HALF_OPEN:
            print("Circuit Breaker: Successful test attempt in HALF-OPEN. Transitioning to CLOSED.")
            self._transition_to(CircuitBreakerState.CLOSED)
        elif self._state == CircuitBreakerState.CLOSED:
            self._failures = 0 # Reset failures if in closed state and success
        
    def _on_failure(self):
        """Called when the wrapped function fails."""
        if self._state == CircuitBreakerState.CLOSED:
            self._failures += 1
            print(f"Circuit Breaker: Failure count: {self._failures}/{self.failure_threshold}")
            if self._failures >= self.failure_threshold:
                print("Circuit Breaker: Failure threshold reached. Transitioning to OPEN.")
                self._transition_to(CircuitBreakerState.OPEN)
        elif self._state == CircuitBreakerState.HALF_OPEN:
            print("Circuit Breaker: Test attempt failed in HALF-OPEN. Transitioning back to OPEN.")
            self._transition_to(CircuitBreakerState.OPEN)

    @property
    def state(self):
        with self._lock:
            return self._state

# --- Example Usage ---

# Simulate a flaky service
service_failures_left = 5
def flaky_service_call():
    global service_failures_left
    if service_failures_left > 0:
        service_failures_left -= 1
        print(f"Service Call: Simulating failure ({service_failures_left} failures left).")
        raise ConnectionError("Service unavailable")
    else:
        print("Service Call: Success!")
        return "Data fetched successfully!"

# Create a circuit breaker instance
my_circuit_breaker = CircuitBreaker(failure_threshold=3, reset_timeout_seconds=5, half_open_test_attempts=1)

# Apply the circuit breaker to the flaky service call
@my_circuit_breaker
def call_service_with_breaker():
    return flaky_service_call()

if __name__ == "__main__":
    print("--- Initial attempts (CLOSED state) ---")
    for i in range(1, 6):
        try:
            print(f"\nAttempt {i}: Current CB State: {my_circuit_breaker.state}")
            result = call_service_with_breaker()
            print(f"Result: {result}")
        except CircuitBreakerError as e:
            print(f"Caught CircuitBreakerError: {e}")
        except ConnectionError as e:
            print(f"Caught original ConnectionError: {e}")
        time.sleep(0.5) # Short delay between attempts

    print("\n--- Waiting for reset timeout ---")
    time.sleep(my_circuit_breaker.reset_timeout_seconds + 1) # Wait longer than reset timeout

    print("\n--- After timeout (HALF-OPEN state) ---")
    # First attempt should trigger HALF-OPEN
    try:
        print(f"\nAttempt 6: Current CB State: {my_circuit_breaker.state}")
        result = call_service_with_breaker()
        print(f"Result: {result}")
    except CircuitBreakerError as e:
        print(f"Caught CircuitBreakerError: {e}")
    except ConnectionError as e:
        print(f"Caught original ConnectionError: {e}")

    # Subsequent attempts should be OPEN again (if the half-open attempt failed)
    print("\n--- Attempts after half-open failure (should be OPEN) ---")
    for i in range(7, 9):
        try:
            print(f"\nAttempt {i}: Current CB State: {my_circuit_breaker.state}")
            result = call_service_with_breaker()
            print(f"Result: {result}")
        except CircuitBreakerError as e:
            print(f"Caught CircuitBreakerError: {e}")
        except ConnectionError as e:
            print(f"Caught original ConnectionError: {e}")
        time.sleep(0.5)

    print("\n--- Waiting for reset timeout again ---")
    service_failures_left = 0 # Make service succeed now
    time.sleep(my_circuit_breaker.reset_timeout_seconds + 1)

    print("\n--- After second timeout (HALF-OPEN, then success to CLOSED) ---")
    try:
        print(f"\nAttempt 9: Current CB State: {my_circuit_breaker.state}")
        result = call_service_with_breaker()
        print(f"Result: {result}")
    except CircuitBreakerError as e:
        print(f"Caught CircuitBreakerError: {e}")
    except ConnectionError as e:
        print(f"Caught original ConnectionError: {e}")

    print(f"\nFinal CB State: {my_circuit_breaker.state}")