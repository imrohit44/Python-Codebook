''' # **Asynchronous Web Scraper**

This program uses asyncio and aiohttp to fetch the titles of multiple web pages concurrently. This is significantly faster than fetching them one by one because the program can send a new request while waiting for previous ones to respond.

**Concepts:** 
Asynchronous I/O, coroutines, web scraping.

### **How to Run**

**1. Install libraries:**

    pip install aiohttp beautifulsoup4

**2. Save the code and run it from your terminal:**   

    python Program_1.py

'''

import asyncio
import aiohttp
from bs4 import BeautifulSoup
import time

async def fetch_title(session, url):
    """Asynchronously fetches a URL and returns the <title> tag content."""
    try:
        async with session.get(url, timeout=10) as response:
            if response.status == 200:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                return soup.title.string.strip() if soup.title else f"No title found for {url}"
            else:
                return f"Error {response.status} for {url}"
    except Exception as e:
        return f"Failed to fetch {url}: {e}"

async def main():
    """Main coroutine to run the web scraper."""
    urls = [
        'https://www.python.org',
        'https://www.google.com',
        'https://www.github.com',
        'https://www.wikipedia.org',
        'https://www.stackoverflow.com'
    ]

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_title(session, url) for url in urls]
        titles = await asyncio.gather(*tasks)
        for url, title in zip(urls, titles):
            print(f"URL: {url}\nTitle: {title}\n")

if __name__ == "__main__":
    print("Starting asynchronous web scraper...")
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    print(f"Completed in {end_time - start_time:.2f} seconds.")