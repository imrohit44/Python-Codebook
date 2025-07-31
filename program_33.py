# To run this problem, you need to install the websockets library:
# pip install websockets

import asyncio
import websockets
import json
import sys
import threading
import time

# --- Server Code ---
class WebSocketChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.connected_clients = set() # Store connected WebSocket objects
        self.lock = asyncio.Lock() # Protect access to connected_clients

    async def _register(self, websocket):
        """Registers a new client connection."""
        async with self.lock:
            self.connected_clients.add(websocket)
            print(f"[Server] Client {websocket.remote_address} connected. Total: {len(self.connected_clients)}")

    async def _unregister(self, websocket):
        """Unregisters a disconnected client."""
        async with self.lock:
            self.connected_clients.remove(websocket)
            print(f"[Server] Client {websocket.remote_address} disconnected. Total: {len(self.connected_clients)}")

    async def _broadcast_message(self, sender_ws, message):
        """Sends a message to all connected clients except the sender."""
        async with self.lock:
            if not self.connected_clients:
                return # No one to send to

            # Prepare message payload
            payload = json.dumps({
                "type": "chat_message",
                "sender": f"{sender_ws.remote_address[0]}:{sender_ws.remote_address[1]}",
                "message": message,
                "timestamp": time.time()
            })
            
            # Send to all other clients concurrently
            tasks = [
                client.send(payload) for client in self.connected_clients if client != sender_ws
            ]
            await asyncio.gather(*tasks)
            print(f"[Server] Broadcasted message from {sender_ws.remote_address}: {message}")

    async def _handler(self, websocket, path):
        """Handles a single client connection."""
        await self._register(websocket)
        try:
            async for message in websocket:
                # print(f"[Server] Received from {websocket.remote_address}: {message}")
                await self._broadcast_message(websocket, message)
        except websockets.exceptions.ConnectionClosedOK:
            print(f"[Server] Connection from {websocket.remote_address} closed normally.")
        except websockets.exceptions.ConnectionClosedError as e:
            print(f"[Server] Connection from {websocket.remote_address} closed with error: {e}")
        except Exception as e:
            print(f"[Server] Error handling client {websocket.remote_address}: {e}")
        finally:
            await self._unregister(websocket)

    async def start(self):
        print(f"WebSocket Chat Server starting on ws://{self.host}:{self.port}")
        self.server = await websockets.serve(self._handler, self.host, self.port)
        await self.server.wait_closed() # Keep server running until explicitly stopped

    async def stop(self):
        if self.server:
            print("[Server] Shutting down WebSocket server...")
            self.server.close()
            await self.server.wait_closed()
            print("[Server] Server stopped.")

# --- Client Code ---
class WebSocketChatClient:
    def __init__(self, uri):
        self.uri = uri
        self.websocket = None
        self.running = True
        self.message_lock = threading.Lock() # For clean console output

    async def _receive_loop(self):
        """Async task to continuously receive messages from the server."""
        try:
            while self.running:
                if self.websocket:
                    message_str = await self.websocket.recv()
                    message = json.loads(message_str)
                    if message.get("type") == "chat_message":
                        sender = message.get("sender", "Unknown")
                        content = message.get("message", "")
                        with self.message_lock:
                            print(f"\n[{sender}] {content}\n> ", end="")
                            sys.stdout.flush() # Ensure prompt is visible after message
                else:
                    await asyncio.sleep(0.1) # Wait if not connected yet
        except websockets.exceptions.ConnectionClosed:
            with self.message_lock:
                print("Connection closed by server.")
            self.running = False
        except Exception as e:
            with self.message_lock:
                print(f"Error in receive loop: {e}")
            self.running = False

    def _send_loop_sync(self):
        """Synchronous thread to read input and send messages."""
        asyncio.set_event_loop(self.loop) # Set event loop for this thread
        while self.running:
            try:
                with self.message_lock:
                    message = input("> ")
                if message.lower() == 'exit':
                    self.stop_sync()
                    break
                if self.websocket and self.websocket.open:
                    # Run the async send operation from sync thread
                    asyncio.run_coroutine_threadsafe(self.websocket.send(message), self.loop)
                else:
                    with self.message_lock:
                        print("Not connected to server. Please wait.")
            except EOFError: # Handles Ctrl+D on Unix-like systems
                self.stop_sync()
                break
            except Exception as e:
                with self.message_lock:
                    print(f"Error sending message: {e}")
                self.stop_sync()
                break
        with self.message_lock:
            print("Client send loop stopped.")

    async def start_async(self):
        """Starts the asynchronous client operations."""
        try:
            self.websocket = await websockets.connect(self.uri)
            print(f"Connected to WebSocket server: {self.uri}")
            
            # Start the receive loop as an asyncio task
            self.receive_task = asyncio.create_task(self._receive_loop())

            # The send loop runs in a separate thread because input() is blocking
            self.loop = asyncio.get_running_loop() # Get current event loop
            self.send_thread = threading.Thread(target=self._send_loop_sync, daemon=True)
            self.send_thread.start()

            # Keep client running until `self.running` becomes False
            while self.running:
                await asyncio.sleep(0.1)

        except websockets.exceptions.ConnectionRefused as e:
            print(f"Connection refused: {e}. Is the server running?")
        except Exception as e:
            print(f"Error connecting to server: {e}")
        finally:
            await self.stop_async()

    def stop_sync(self):
        """Stops the client from a synchronous context (e.g., input thread)."""
        print("Shutting down client...")
        self.running = False
        # The async stop will be called once `start_async`'s loop detects `self.running` is False.

    async def stop_async(self):
        """Performs asynchronous cleanup."""
        if self.receive_task and not self.receive_task.done():
            self.receive_task.cancel()
            try: await self.receive_task
            except asyncio.CancelledError: pass # Expected
        
        if self.websocket and self.websocket.open:
            await self.websocket.close()
        
        # Give send thread a moment to finish, if it's not daemon
        if self.send_thread and self.send_thread.is_alive():
            # For this simple example, we rely on daemon=True for the send_thread
            # or the main program's exit. In more complex scenarios, you'd need
            # a more robust way to signal it to exit.
            pass 
        print("Client stopped.")

# --- Main entry point to run server or client ---
async def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Server: python your_script.py server <port>")
        print("  Client: python your_script.py client <server_ip> <server_port>")
        sys.exit(1)

    command = sys.argv[1]

    if command == "server":
        port = int(sys.argv[2])
        server = WebSocketChatServer("0.0.0.0", port) # Listen on all interfaces
        await server.start()
    elif command == "client":
        if len(sys.argv) < 4:
            print("Usage: python your_script.py client <server_ip> <server_port>")
            sys.exit(1)
        server_ip = sys.argv[2]
        server_port = int(sys.argv[3])
        client_uri = f"ws://{server_ip}:{server_port}"
        client = WebSocketChatClient(client_uri)
        await client.start_async()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    # To test:
    # 1. Open Terminal 1: python your_script_name.py server 8765
    # 2. Open Terminal 2: python your_script_name.py client 127.0.0.1 8765
    # 3. Open Terminal 3: python your_script_name.py client 127.0.0.1 8765
    # Now type messages in any client terminal, and they should appear in others.
    asyncio.run(main())