import asyncio
import time

class GameObject:
    def __init__(self, name):
        self.name = name
        self.is_active = True
        self.events = asyncio.Queue()

    async def run(self):
        while self.is_active:
            await self.tick()
            try:
                event = self.events.get_nowait()
                await self.handle_event(event)
                self.events.task_done()
            except asyncio.QueueEmpty:
                pass

    async def tick(self):
        await asyncio.sleep(0)

    async def handle_event(self, event):
        pass

class GameLoop:
    def __init__(self, fps):
        self.fps = fps
        self.game_objects = []
        self.event_bus = asyncio.Queue()
        self.tasks = []
        self.is_running = False

    def add_object(self, obj):
        self.game_objects.append(obj)

    async def _update_loop(self):
        frame_time = 1 / self.fps
        while self.is_running:
            start_time = time.time()
            for obj in self.game_objects:
                obj.tick()
            
            end_time = time.time()
            sleep_time = frame_time - (end_time - start_time)
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)

    async def _event_dispatcher(self):
        while self.is_running:
            event = await self.event_bus.get()
            for obj in self.game_objects:
                await obj.events.put(event)
            self.event_bus.task_done()

    async def start(self):
        self.is_running = True
        self.tasks.append(asyncio.create_task(self._update_loop()))
        self.tasks.append(asyncio.create_task(self._event_dispatcher()))
        self.tasks.extend([asyncio.create_task(obj.run()) for obj in self.game_objects])

        while self.is_running:
            await asyncio.sleep(1)

    async def stop(self):
        self.is_running = False
        for task in self.tasks:
            task.cancel()
        await asyncio.gather(*self.tasks, return_exceptions=True)

class Player(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.x = 0
        self.y = 0

    async def tick(self):
        print(f"Player {self.name} is at ({self.x}, {self.y})")
        
    async def handle_event(self, event):
        if event['type'] == 'move':
            self.x += event['dx']
            self.y += event['dy']

async def main():
    engine = GameLoop(fps=60)
    player1 = Player('P1')
    engine.add_object(player1)
    
    engine_task = asyncio.create_task(engine.start())

    await asyncio.sleep(1)
    await engine.event_bus.put({'type': 'move', 'dx': 1, 'dy': 1})
    await asyncio.sleep(1)
    await engine.event_bus.put({'type': 'move', 'dx': -1, 'dy': 0})
    await asyncio.sleep(1)

    await engine.stop()

if __name__ == '__main__':
    asyncio.run(main())