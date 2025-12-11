import asyncio
import time
import random

class Resource:
    def __init__(self, id):
        self.id = id
        self.in_use = False

    async def use(self):
        self.in_use = True
        await asyncio.sleep(random.uniform(0.1, 0.5))
        self.in_use = False

class AsyncResourcePool:
    def __init__(self, pool_size):
        self.pool_size = pool_size
        self.available_resources = asyncio.Queue(maxsize=pool_size)
        self.semaphore = asyncio.Semaphore(pool_size)
        
        for i in range(pool_size):
            self.available_resources.put_nowait(Resource(i))

    async def checkout(self):
        await self.semaphore.acquire()
        resource = await self.available_resources.get()
        print(f"Checkout: Resource {resource.id} acquired.")
        return resource

    async def checkin(self, resource):
        await self.available_resources.put(resource)
        self.semaphore.release()
        print(f"Checkin: Resource {resource.id} released.")

async def database_task(pool, task_id):
    resource = None
    try:
        print(f"Task {task_id}: Waiting for resource...")
        resource = await pool.checkout()
        
        print(f"Task {task_id}: Using Resource {resource.id}")
        await resource.use()
        
    finally:
        if resource:
            await pool.checkin(resource)

async def main():
    pool_size = 3
    pool = AsyncResourcePool(pool_size)
    
    tasks = [asyncio.create_task(database_task(pool, i)) for i in range(5)]
    
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())