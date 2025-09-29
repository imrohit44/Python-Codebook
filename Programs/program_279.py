import threading
import queue
import time
import concurrent.futures

class PriorityThreadPoolExecutor:
    def __init__(self, max_workers):
        self._max_workers = max_workers
        self._work_queue = queue.PriorityQueue()
        self._threads = []
        self._running = True
        
        for _ in range(max_workers):
            t = threading.Thread(target=self._worker_run, daemon=True)
            self._threads.append(t)
            t.start()

    def _worker_run(self):
        while self._running:
            try:
                priority, task_id, future, fn, args, kwargs = self._work_queue.get(timeout=0.1)
                
                if future.set_running_or_notify_cancel():
                    try:
                        result = fn(*args, **kwargs)
                        future.set_result(result)
                    except Exception as e:
                        future.set_exception(e)
                    finally:
                        self._work_queue.task_done()
            except queue.Empty:
                continue

    def submit(self, fn, *args, priority=0, **kwargs):
        future = concurrent.futures.Future()
        task_id = time.time()
        # PriorityQueue is min-heap, so negate priority for max-heap behavior
        self._work_queue.put((-priority, task_id, future, fn, args, kwargs)) 
        return future

    def shutdown(self, wait=True):
        self._running = False
        if wait:
            self._work_queue.join()
            for t in self._threads:
                t.join()

def heavy_task(task_name, duration):
    print(f"[{task_name}] Starting (P={priority_map[task_name]})...")
    time.sleep(duration)
    print(f"[{task_name}] Finished.")
    return f"{task_name} done"

priority_map = {'High': 10, 'Medium': 5, 'Low': 1}

if __name__ == '__main__':
    executor = PriorityThreadPoolExecutor(max_workers=2)
    
    # Submit tasks out of priority order
    executor.submit(heavy_task, 'Medium', 1.5, priority=priority_map['Medium'])
    executor.submit(heavy_task, 'Low', 2.0, priority=priority_map['Low'])
    f_high = executor.submit(heavy_task, 'High', 1.0, priority=priority_map['High'])
    
    print(f"High-priority result: {f_high.result()}")
    
    executor.shutdown()