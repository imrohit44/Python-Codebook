import time
from multiprocessing.dummy import Pool as ThreadPool # GIL-less simulation

class SharedResource:
    def __init__(self):
        self.counter = 0
        self.lock = threading.Lock()

    def increment_safe(self, count):
        # I/O or CPU-bound tasks still benefit from thread-based concurrency even with GIL
        time.sleep(0.001) 
        with self.lock:
            for _ in range(count):
                self.counter += 1
                
    def increment_unsafe(self, count):
        # Without GIL/lock, this would be race condition territory
        for _ in range(count):
            self.counter += 1

def worker_safe(resource, count):
    resource.increment_safe(count)

def worker_unsafe(resource, count):
    resource.increment_unsafe(count)

if __name__ == '__main__':
    NUM_WORKERS = 4
    INCREMENT_COUNT = 50000 
    
    # Simulate a scenario where locks manage critical sections
    safe_resource = SharedResource()
    start_time_safe = time.time()
    
    with ThreadPool(NUM_WORKERS) as pool:
        pool.starmap(worker_safe, [(safe_resource, INCREMENT_COUNT) for _ in range(NUM_WORKERS)])
    
    end_time_safe = time.time()
    print(f"Safe Count (Target: {NUM_WORKERS * INCREMENT_COUNT}): {safe_resource.counter}")
    print(f"Safe Execution Time: {end_time_safe - start_time_safe:.4f}s")

    # Simulate pure race condition (Unsafe)
    unsafe_resource = SharedResource()
    start_time_unsafe = time.time()
    
    with ThreadPool(NUM_WORKERS) as pool:
        pool.starmap(worker_unsafe, [(unsafe_resource, INCREMENT_COUNT) for _ in range(NUM_WORKERS)])
        
    end_time_unsafe = time.time()
    print(f"Unsafe Count (Expected Error): {unsafe_resource.counter}")
    print(f"Unsafe Execution Time: {end_time_unsafe - start_time_unsafe:.4f}s")