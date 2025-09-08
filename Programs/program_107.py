import asyncio
import time
import random

class RateLimiter:
    def __init__(self, requests_per_second, capacity):
        self._requests_per_second = requests_per_second
        self._capacity = capacity
        self._tokens = capacity
        self._last_refill = time.time()
        self._semaphore = asyncio.Semaphore(capacity)

    async def acquire(self):
        now = time.time()
        time_elapsed = now - self._last_refill
        
        new_tokens = int(time_elapsed * self._requests_per_second)
        if new_tokens > 0:
            self._tokens = min(self._capacity, self._tokens + new_tokens)
            self._last_refill = now

        if self._tokens > 0:
            self._tokens -= 1
            return
        
        time_to_wait = (1.0 / self._requests_per_second) - time_elapsed % (1.0 / self._requests_per_second)
        await asyncio.sleep(time_to_wait)
        self._tokens = max(0, self._tokens - 1)

async def make_request(limiter, request_id):
    await limiter.acquire()
    print(f"Request {request_id} acquired lock at {time.time()}")
    await asyncio.sleep(random.uniform(0.1, 0.5))
    print(f"Request {request_id} finished at {time.time()}")

async def main():
    limiter = RateLimiter(requests_per_second=5, capacity=2)
    tasks = [make_request(limiter, i) for i in range(10)]
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())