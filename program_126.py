import asyncio
import random
import time

async def producer(queue, num_items):
    for i in range(num_items):
        item = f"item_{i}"
        print(f"Producer: Producing {item}")
        await queue.put(item)
        await asyncio.sleep(0.5)

async def processor(in_queue, out_queue):
    while True:
        item = await in_queue.get()
        print(f"Processor: Processing {item}")
        await asyncio.sleep(random.uniform(0.1, 0.5))
        result = f"{item}_processed"
        await out_queue.put(result)
        in_queue.task_done()

async def sink(queue):
    while True:
        result = await queue.get()
        print(f"Sink: Consuming {result}")
        await asyncio.sleep(random.uniform(0.5, 1.0))
        queue.task_done()

async def main():
    q1 = asyncio.Queue(maxsize=5)
    q2 = asyncio.Queue(maxsize=3)
    
    producer_task = asyncio.create_task(producer(q1, 10))
    processor_task = asyncio.create_task(processor(q1, q2))
    sink_task = asyncio.create_task(sink(q2))
    
    await producer_task
    await q1.join()
    await q2.join()
    
    processor_task.cancel()
    sink_task.cancel()
    
    await asyncio.gather(processor_task, sink_task, return_exceptions=True)
    
if __name__ == '__main__':
    asyncio.run(main())