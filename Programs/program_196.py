import asyncio
import time

class Machine:
    def __init__(self, name, process_time, input_queue, output_queue):
        self.name = name
        self.process_time = process_time
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.processed_count = 0

    async def run(self):
        print(f"Machine {self.name} started.")
        while True:
            try:
                item = await self.input_queue.get()
                print(f"Machine {self.name} received item {item}. Processing...")
                await asyncio.sleep(self.process_time)
                self.processed_count += 1
                new_item = f"{item} processed by {self.name}"
                if self.output_queue:
                    await self.output_queue.put(new_item)
                print(f"Machine {self.name} finished processing item {item}. Processed: {self.processed_count}")
                self.input_queue.task_done()
            except asyncio.CancelledError:
                print(f"Machine {self.name} shutting down. Processed {self.processed_count} items.")
                break

async def producer(queue, num_items):
    print("Producer started.")
    for i in range(num_items):
        item = f"Raw Item {i + 1}"
        await queue.put(item)
        print(f"Producer produced item {item}.")
        await asyncio.sleep(0.5)
    print("Producer finished.")

async def main():
    q1 = asyncio.Queue()
    q2 = asyncio.Queue()
    q3 = asyncio.Queue()

    p = producer(q1, 10)
    m1 = Machine("Cutter", 0.5, q1, q2)
    m2 = Machine("Press", 1.0, q2, q3)
    m3 = Machine("Finisher", 0.7, q3, None)

    m1_task = asyncio.create_task(m1.run())
    m2_task = asyncio.create_task(m2.run())
    m3_task = asyncio.create_task(m3.run())

    await p
    await q1.join()
    await q2.join()
    await q3.join()

    m1_task.cancel()
    m2_task.cancel()
    m3_task.cancel()

    await asyncio.gather(m1_task, m2_task, m3_task, return_exceptions=True)
    print("All tasks finished.")

if __name__ == '__main__':
    asyncio.run(main())