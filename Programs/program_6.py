import asyncio
import aiohttp

async def fetch_url(session, url):
    try:
        async with session.get(url, timeout=10) as response:
            status = response.status
            text = await response.text()
            print(f"URL: {url}")
            print(f"Status: {status}")
            print(f"Content (first 100 chars): {text[:100]}...")
            print("-" * 30)
    except aiohttp.ClientError as e:
        print(f"Error fetching {url}: {e}")
    except asyncio.TimeoutError:
        print(f"Timeout fetching {url}")

async def main():
    urls = [
        "https://www.google.com",
        "https://www.python.org",
        "https://www.github.com",
        "https://www.example.com",
        "https://nonexistent-domain-12345.com"  # Example of a URL that will fail
    ]

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())