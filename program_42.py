import asyncio

class AsyncConnection:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.is_connected = False

    async def __aenter__(self):
        print("AsyncConnection: Establishing connection...")
        await asyncio.sleep(1)
        self.is_connected = True
        print("AsyncConnection: Connection established.")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("AsyncConnection: Closing connection...")
        await asyncio.sleep(0.5)
        self.is_connected = False
        print("AsyncConnection: Connection closed.")
        if exc_type:
            print(f"An exception occurred during execution: {exc_val}")
        return False

async def main():
    print("Main: Starting async operations.")
    async with AsyncConnection('localhost', 8080) as conn:
        print(f"Main: Inside context manager. Connected: {conn.is_connected}")
        await asyncio.sleep(2)
        print("Main: Inside context manager. Simulating more work.")
    print("Main: After context manager.")

    try:
        async with AsyncConnection('localhost', 8080) as conn_with_error:
            print(f"Main: Inside context with error. Connected: {conn_with_error.is_connected}")
            raise ValueError("A simulated error occurred.")
    except ValueError as e:
        print(f"Main: Caught expected error: {e}")

if __name__ == "__main__":
    asyncio.run(main())