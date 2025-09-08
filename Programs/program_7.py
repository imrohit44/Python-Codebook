import time

class Timer:
    def __enter__(self):
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        end_time = time.perf_counter()
        elapsed_time = end_time - self.start_time
        print(f"Code block executed in {elapsed_time:.4f} seconds.")
        # Returning False (or not returning anything) propagates exceptions
        # Returning True suppresses exceptions

print("Starting simulation...")
with Timer():
    # Simulate some work
    time.sleep(2.5)
    result = sum(range(10**6))
    print(f"Sum calculated: {result}")
print("Simulation finished.")

print("\nAnother example with a shorter task:")
with Timer():
    data = [i * i for i in range(100000)]