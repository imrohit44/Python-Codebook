'''
# Concurrent Downloader with concurrent.futures

This program revisits the idea of a concurrent downloader but uses the high-level concurrent.futures module with a ThreadPoolExecutor. This is often a more modern and readable way to handle I/O-bound concurrency (like network requests) compared to using the lower-level threading or multiprocessing modules directly.

Concepts: Concurrency, thread pools, future objects, I/O-bound tasks.

**How to Run**

**1. Save the code and execute it:**

```
python Program_12.py
```
'''

import requests
import concurrent.futures
import time

# List of URLs to download (small text files for speed)
URLS = [
    "https://www.rfc-editor.org/rfc/rfc2616.txt", # HTTP/1.1
    "https://www.rfc-editor.org/rfc/rfc793.txt",  # TCP
    "https://www.rfc-editor.org/rfc/rfc791.txt",  # IP
    "https://www.rfc-editor.org/rfc/rfc821.txt",  # SMTP
    "https://www.rfc-editor.org/rfc/rfc20.txt",   # ASCII format
]

def download_url(url):
    """Downloads content from a URL and returns its length."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        print(f"Downloaded {url} [{len(response.content)} bytes]")
        return url, len(response.content)
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}")
        return url, -1 # Indicate failure

def main():
    print("--- Starting Sequential Download ---")
    start_time_seq = time.time()
    for url in URLS:
        download_url(url)
    end_time_seq = time.time()
    print(f"Sequential download finished in {end_time_seq - start_time_seq:.2f} seconds.\n")

    print("--- Starting Concurrent Download with ThreadPoolExecutor ---")
    start_time_con = time.time()
    # Create a thread pool with a max of 5 workers
    # The 'with' statement ensures threads are cleaned up properly
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # 'map' applies the function to each item in the iterable
        # and returns the results as they are completed.
        results = executor.map(download_url, URLS)
    
    # You can process results here if needed
    for url, length in results:
        pass # The work is already done and printed inside download_url

    end_time_con = time.time()
    print(f"Concurrent download finished in {end_time_con - start_time_con:.2f} seconds.")

if __name__ == "__main__":
    main()