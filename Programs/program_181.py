import asyncio
import websockets
import json

class LockManager:
    def __init__(self):
        self.locks = {}
        self.queue = asyncio.Queue()

    async def handle_client(self, websocket, path):
        try:
            async for message in websocket:
                msg = json.loads(message)
                action, lock_name = msg['action'], msg['lock_name']
                
                if action == 'acquire':
                    if lock_name not in self.locks:
                        self.locks[lock_name] = websocket
                        await websocket.send(json.dumps({'status': 'granted'}))
                    else:
                        await self.queue.put((lock_name, websocket))
                
                elif action == 'release':
                    if self.locks.get(lock_name) == websocket:
                        del self.locks[lock_name]
                        if not self.queue.empty():
                            await self._grant_queued_lock()
        except websockets.exceptions.ConnectionClosedError:
            pass
        finally:
            for lock_name, holder in list(self.locks.items()):
                if holder == websocket:
                    del self.locks[lock_name]
                    if not self.queue.empty():
                        await self._grant_queued_lock()

    async def _grant_queued_lock(self):
        try:
            lock_name, client_ws = self.queue.get_nowait()
            if lock_name not in self.locks:
                self.locks[lock_name] = client_ws
                await client_ws.send(json.dumps({'status': 'granted'}))
        except asyncio.QueueEmpty:
            pass

    async def start(self):
        server = await websockets.serve(self.handle_client, 'localhost', 8765)
        print("Lock Manager started on ws://localhost:8765")
        await server.wait_closed()

async def client(client_id):
    uri = "ws://localhost:8765"
    try:
        async with websockets.connect(uri) as websocket:
            print(f"Client {client_id}: Requesting lock.")
            await websocket.send(json.dumps({'action': 'acquire', 'lock_name': 'my_lock'}))
            
            response = json.loads(await websocket.recv())
            if response['status'] == 'granted':
                print(f"Client {client_id}: Acquired lock. Doing work...")
                await asyncio.sleep(random.uniform(1, 3))
                
                print(f"Client {client_id}: Releasing lock.")
                await websocket.send(json.dumps({'action': 'release', 'lock_name': 'my_lock'}))
    except websockets.exceptions.ConnectionRefusedError:
        print("Connection refused. Is the Lock Manager running?")

async def main():
    manager = LockManager()
    manager_task = asyncio.create_task(manager.start())
    
    await asyncio.sleep(1)
    
    client_tasks = [asyncio.create_task(client(i)) for i in range(3)]
    await asyncio.gather(*client_tasks)
    
    manager_task.cancel()
    await manager_task

if __name__ == '__main__':
    asyncio.run(main())