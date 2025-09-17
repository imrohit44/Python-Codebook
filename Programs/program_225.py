import threading

class CustomFuture:
    def __init__(self):
        self._result = None
        self._callbacks = []
        self._state = 'pending'
        self._lock = threading.Lock()

    def set_result(self, result):
        with self._lock:
            if self._state != 'pending':
                raise RuntimeError("Result already set")
            self._result = result
            self._state = 'finished'
            for callback in self._callbacks:
                callback(self)

    def add_done_callback(self, callback):
        with self._lock:
            if self._state == 'finished':
                callback(self)
            else:
                self._callbacks.append(callback)

    def result(self):
        with self._lock:
            if self._state != 'finished':
                raise RuntimeError("Result not available")
            return self._result

def worker_task(future):
    time.sleep(2)
    future.set_result("Task finished")

def main():
    future = CustomFuture()
    
    def callback(f):
        print(f"Callback received result: {f.result()}")

    future.add_done_callback(callback)
    
    worker_thread = threading.Thread(target=worker_task, args=(future,))
    worker_thread.start()
    
    print("Main thread waiting for result...")
    worker_thread.join()
    
if __name__ == '__main__':
    main()