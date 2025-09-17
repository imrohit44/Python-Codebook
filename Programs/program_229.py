import asyncio
import time

async def client(reader, writer):
    print("Client: Sending ClientHello...")
    writer.write(b"ClientHello\n")
    
    server_hello = await reader.readline()
    print(f"Client: Received {server_hello.decode().strip()}")
    
    server_certificate = await reader.readline()
    print(f"Client: Received {server_certificate.decode().strip()}")
    
    print("Client: Sending ClientKeyExchange...")
    writer.write(b"ClientKeyExchange\n")
    
    finished = await reader.readline()
    print(f"Client: Received {finished.decode().strip()}")

    print("Client: Handshake complete.")

async def server(reader, writer):
    client_hello = await reader.readline()
    print(f"Server: Received {client_hello.decode().strip()}")
    
    print("Server: Sending ServerHello...")
    writer.write(b"ServerHello\n")
    
    print("Server: Sending ServerCertificate...")
    writer.write(b"ServerCertificate\n")
    
    client_key_exchange = await reader.readline()
    print(f"Server: Received {client_key_exchange.decode().strip()}")
    
    print("Server: Sending Finished...")
    writer.write(b"Finished\n")

    print("Server: Handshake complete.")
    
async def main():
    server_task = await asyncio.start_server(server, '127.0.0.1', 8888)
    client_task = asyncio.open_connection('127.0.0.1', 8888)
    
    await asyncio.gather(server_task.wait_closed(), client_task)

if __name__ == '__main__':
    asyncio.run(main())