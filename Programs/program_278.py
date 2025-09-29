import time

class RateLimiter:
    def __init__(self, max_calls_per_sec):
        self.interval = 1.0 / max_calls_per_sec
        self.last_call_time = 0
        self.lock = threading.Lock()

    def acquire(self):
        with self.lock:
            time_to_wait = self.last_call_time + self.interval - time.time()
            if time_to_wait > 0:
                time.sleep(time_to_wait)
            self.last_call_time = time.time()

class Proxy:
    def __init__(self, target):
        object.__setattr__(self, '_target', target)
        object.__setattr__(self, '_limiter', RateLimiter(max_calls_per_sec=2))

    def __getattr__(self, name):
        attr = getattr(self._target, name)
        
        if callable(attr):
            def wrapper(*args, **kwargs):
                self._limiter.acquire()
                print(f"--- Proxy: Intercepted and Throttled {name} ---")
                return attr(*args, **kwargs)
            return wrapper
        
        return attr

    def __setattr__(self, name, value):
        setattr(self._target, name, value)

class ExternalService:
    def fetch_data(self, user_id):
        return f"Data for {user_id} fetched at {time.strftime('%H:%M:%S')}"
    
    def log_status(self, status):
        print(f"Service status: {status}")

if __name__ == '__main__':
    service = ExternalService()
    proxy = Proxy(service)
    
    for i in range(5):
        print(proxy.fetch_data(i))