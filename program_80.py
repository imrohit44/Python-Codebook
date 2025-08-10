import asyncio
import time

async def api_gateway(request_queue, response_queue):
    while True:
        try:
            request = await request_queue.get(timeout=1)
            request_id, payload = request
            print(f"Gateway received request {request_id}")
            
            await response_queue.put((request_id, payload * 2))
            
            print(f"Gateway sent response for {request_id}")
        except asyncio.TimeoutError:
            continue

async def worker_service(request_queue, response_queue):
    while True:
        try:
            request = await request_queue.get(timeout=1)
            request_id, payload = request
            print(f"Worker received request {request_id}")
            
            await asyncio.sleep(0.5)
            
            await response_queue.put((request_id, payload + 1))
            
            print(f"Worker finished request {request_id}")
        except asyncio.TimeoutError:
            continue

async def client_service(request_queue, response_queue):
    for i in range(5):
        request_id = i + 1
        payload = i * 10
        await request_queue.put((request_id, payload))
        print(f"Client sent request {request_id} with payload {payload}")
        
    await asyncio.sleep(2)
    
    results = {}
    while not response_queue.empty():
        request_id, result = response_queue.get_nowait()
        results[request_id] = result
    
    print("--- Results ---")
    for rid, res in results.items():
        print(f"Request {rid}: {res}")

async def main():
    api_to_worker = asyncio.Queue()
    worker_to_api = asyncio.Queue()
    
    client_task = asyncio.create_task(client_service(api_to_worker, worker_to_api))
    gateway_task = asyncio.create_task(api_gateway(api_to_worker, worker_to_api))
    worker_task = asyncio.create_task(worker_service(api_to_worker, worker_to_api))

    await client_task
    
    gateway_task.cancel()
    worker_task.cancel()
    
    await asyncio.gather(gateway_task, worker_task, return_exceptions=True)

if __name__ == '__main__':
    asyncio.run(main())