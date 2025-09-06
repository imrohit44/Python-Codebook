import asyncio
import heapq
import time

class TaskScheduler:
    def __init__(self):
        self._queue = []
        self._task_id_counter = 0

    async def run(self):
        print("Scheduler started.")
        while True:
            if not self._queue:
                await asyncio.sleep(0.1)
                continue
            
            _, _, coro = heapq.heappop(self._queue)
            
            try:
                await coro
            except asyncio.CancelledError:
                pass

    def schedule(self, coro, priority=0):
        self._task_id_counter += 1
        heapq.heappush(self._queue, (-priority, self._task_id_counter, coro))
        print(f"Scheduled task with priority {priority}")

async def simple_task(task_id, duration):
    print(f"Task {task_id} started (duration: {duration}s)")
    await asyncio.sleep(duration)
    print(f"Task {task_id} finished.")

async def main():
    scheduler = TaskScheduler()
    scheduler_task = asyncio.create_task(scheduler.run())

    scheduler.schedule(simple_task('A', 2), priority=10)
    scheduler.schedule(simple_task('B', 1), priority=20)
    scheduler.schedule(simple_task('C', 3), priority=5)

    await asyncio.sleep(5)
    scheduler_task.cancel()
    try:
        await scheduler_task
    except asyncio.CancelledError:
        print("Scheduler stopped.")

if __name__ == '__main__':
    asyncio.run(main())