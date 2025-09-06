import asyncio
import random
import time

async def producer(queue: asyncio.Queue, producer_id: int, num_items: int):
    """
    Asynchronous producer function.
    Generates items and puts them into the queue, applying backpressure.
    """
    print(f"Producer {producer_id}: Starting...")
    for i in range(1, num_items + 1):
        item = f"Producer {producer_id}-Item {i}"
        try:
            # Try to put item. If queue is full, this will wait until space is available.
            # This is how backpressure is applied.
            await queue.put(item) 
            print(f"Producer {producer_id}: Put '{item}' (Queue size: {queue.qsize()})")
        except asyncio.CancelledError:
            print(f"Producer {producer_id}: Cancelled.")
            break
        except Exception as e:
            print(f"Producer {producer_id}: Error putting item: {e}")
            break
        
        # Simulate variable work before producing next item
        await asyncio.sleep(random.uniform(0.1, 0.5)) 
    print(f"Producer {producer_id}: Finished producing.")

async def consumer(queue: asyncio.Queue, consumer_id: int):
    """
    Asynchronous consumer function.
    Takes items from the queue and processes them.
    """
    print(f"Consumer {consumer_id}: Starting...")
    while True:
        try:
            # Try to get item. If queue is empty, this will wait until an item is available.
            item = await queue.get()
            print(f"Consumer {consumer_id}: Got '{item}' (Queue size: {queue.qsize()})")
            
            # Simulate variable processing time
            await asyncio.sleep(random.uniform(0.5, 1.5)) 
            
            queue.task_done() # Mark the task as done
            print(f"Consumer {consumer_id}: Processed '{item}'.")
        except asyncio.CancelledError:
            print(f"Consumer {consumer_id}: Cancelled.")
            break
        except Exception as e:
            print(f"Consumer {consumer_id}: Error getting/processing item: {e}")
            break
    print(f"Consumer {consumer_id}: Finished consuming.")

async def main():
    queue_capacity = 5 # Small capacity to demonstrate backpressure
    num_producers = 3
    num_consumers = 2
    items_per_producer = 5

    message_queue = asyncio.Queue(maxsize=queue_capacity)
    print(f"Initialized Async Queue with max size: {queue_capacity}")

    # Create and start producer tasks
    producer_tasks = [
        asyncio.create_task(producer(message_queue, i + 1, items_per_producer))
        for i in range(num_producers)
    ]

    # Create and start consumer tasks
    consumer_tasks = [
        asyncio.create_task(consumer(message_queue, i + 1))
        for i in range(num_consumers)
    ]

    # Wait for all producers to finish.
    # The `await asyncio.gather(*producer_tasks)` will ensure all producers complete.
    await asyncio.gather(*producer_tasks)
    print("\nAll producers have finished.")

    # Wait for all items in the queue to be processed by consumers.
    # `await message_queue.join()` will block until all items that were put into the queue
    # are retrieved and their `task_done()` method is called.
    print("Waiting for all queued items to be processed...")
    await message_queue.join()
    print("All items in queue have been processed.")

    # Cancel consumer tasks (they run indefinitely)
    print("Cancelling consumer tasks...")
    for task in consumer_tasks:
        task.cancel()
    # Wait for consumer tasks to finish cancelling
    await asyncio.gather(*consumer_tasks, return_exceptions=True) 
    
    print("\nSimulation complete.")

if __name__ == "__main__":
    start_time = time.monotonic()
    asyncio.run(main())
    end_time = time.monotonic()
    print(f"Total simulation time: {end_time - start_time:.2f} seconds.")