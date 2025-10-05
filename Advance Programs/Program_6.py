'''
# Real-time Chat Application with WebSockets

This example creates a simple, multi-client chat room using the websockets library. A central server receives messages from one client and broadcasts them to all other connected clients in real-time.

**Concepts:**  

WebSockets, asynchronous programming, real-time communication.

**How to Run**

**1. Save the code and execute it:**

```
python Program_6.py
```
'''

import asyncio
import websockets

# A set to store all connected client websockets
CONNECTED_CLIENTS = set()

async def register(websocket):
    """Adds a new client to the set of connected clients."""
    CONNECTED_CLIENTS.add(websocket)
    print(f"New connection: {websocket.remote_address}. Total clients: {len(CONNECTED_CLIENTS)}")

async def unregister(websocket):
    """Removes a client from the set."""
    CONNECTED_CLIENTS.remove(websocket)
    print(f"Connection closed: {websocket.remote_address}. Total clients: {len(CONNECTED_CLIENTS)}")

async def broadcast_message(message):
    """Sends a message to all connected clients."""
    if CONNECTED_CLIENTS:
        # Create a list of tasks for sending the message
        tasks = [client.send(message) for client in CONNECTED_CLIENTS]
        await asyncio.gather(*tasks)

async def chat_handler(websocket, path):
    """Handles incoming messages from a client and broadcasts them."""
    await register(websocket)
    try:
        async for message in websocket:
            print(f"Received message from {websocket.remote_address}: {message}")
            await broadcast_message(message)
    finally:
        await unregister(websocket)

async def main():
    """Starts the WebSocket chat server."""
    server_address = "localhost"
    server_port = 8765
    async with websockets.serve(chat_handler, server_address, server_port):
        print(f"Chat server started on ws://{server_address}:{server_port}")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())