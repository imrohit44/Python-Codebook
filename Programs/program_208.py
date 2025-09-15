import asyncio
import threading
import time

def run_event_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

class AsyncExecutor:
    def __init__(self):
        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(target=run_event_loop, args=(self._loop,), daemon=True)
        self._thread.start()

    def submit_task(self, coro):
        future = asyncio.run_coroutine_threadsafe(coro, self._loop)
        return future.result()

async def worker_task(task_id):
    print(f"Task {task_id} started on thread {threading.get_ident()}")
    await asyncio.sleep(1)
    return f"Task {task_id} finished"

def main():
    executor = AsyncExecutor()
    
    print(f"Main thread: {threading.get_ident()}")
    
    result1 = executor.submit_task(worker_task(1))
    print(f"Result 1: {result1}")
    
    result2 = executor.submit_task(worker_task(2))
    print(f"Result 2: {result2}")
    
if __name__ == '__main__':
    main()