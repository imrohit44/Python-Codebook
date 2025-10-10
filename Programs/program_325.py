import asyncio
import time

class AsyncBarrier:
    def __init__(self, num_participants):
        self.num_participants = num_participants
        self.participants = 0
        self.event = asyncio.Event()

    async def wait(self):
        self.participants += 1
        
        if self.participants < self.num_participants:
            await self.event.wait()
        else:
            self.event.set()

async def worker(barrier, worker_id, start_time):
    print(f"Worker {worker_id}: Started.")
    await asyncio.sleep(random.uniform(0.1, 0.5))
    
    print(f"Worker {worker_id}: Arrived at barrier at {time.time() - start_time:.2f}s")
    await barrier.wait()
    
    print(f"Worker {worker_id}: Passed barrier at {time.time() - start_time:.2f}s")

async def main():
    start_time = time.time()
    barrier = AsyncBarrier(3)
    
    tasks = [asyncio.create_task(worker(barrier, i, start_time)) for i in range(1, 4)]
    
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())