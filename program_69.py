import asyncio
import time

async def source(queue, num_items):
    for i in range(num_items):
        item = f"item_{i}"
        print(f"Source: Producing {item}")
        await queue.put(item)
        await asyncio.sleep(0.1)

async def processor(in_queue, out_queue, process_time):
    while True:
        item = await in_queue.get()
        print(f"Processor: Processing {item}")
        await asyncio.sleep(process_time)
        result = f"{item}_processed"
        await out_queue.put(result)
        in_queue.task_done()

async def sink(queue):
    while True:
        result = await queue.get()
        print(f"Sink: Consuming {result}")
        await asyncio.sleep(1)
        queue.task_done()

async def main():
    q1 = asyncio.Queue(maxsize=5)
    q2 = asyncio.Queue(maxsize=3)
    
    producer_task = asyncio.create_task(source(q1, 15))
    processor_task = asyncio.create_task(processor(q1, q2, 0.5))
    sink_task = asyncio.create_task(sink(q2))
    
    await producer_task
    await q1.join()
    await q2.join()
    
    processor_task.cancel()
    sink_task.cancel()
    
    await asyncio.gather(processor_task, sink_task, return_exceptions=True)

if __name__ == "__main__":
    asyncio.run(main())