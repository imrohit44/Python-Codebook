import asyncio
import time
import random

async def producer(queue, num_items):
    for i in range(num_items):
        item = f"item_{i}"
        await queue.put(item)
        print(f"Producer produced {item}")
        await asyncio.sleep(0.5)
    await queue.put(None)

async def worker(worker_id, in_queue, out_queue):
    while True:
        item = await in_queue.get()
        if item is None:
            await in_queue.put(None)
            await out_queue.put(None)
            break
            
        print(f"Worker {worker_id}: Processing {item}")
        await asyncio.sleep(random.uniform(0.1, 0.5))
        result = f"{item}_processed_by_worker_{worker_id}"
        await out_queue.put(result)
        in_queue.task_done()

async def sink(queue):
    while True:
        result = await queue.get()
        if result is None:
            await queue.put(None)
            break
        print(f"Sink: Consumed {result}")
        await asyncio.sleep(0.2)
        queue.task_done()

async def main():
    q1 = asyncio.Queue()
    q2 = asyncio.Queue()
    
    producer_task = asyncio.create_task(producer(q1, 10))
    workers = [asyncio.create_task(worker(i, q1, q2)) for i in range(3)]
    sink_task = asyncio.create_task(sink(q2))

    await producer_task
    await q1.join()
    await q2.join()

    for w in workers:
        w.cancel()
    
    await asyncio.gather(*workers, sink_task, return_exceptions=True)

if __name__ == "__main__":
    asyncio.run(main())