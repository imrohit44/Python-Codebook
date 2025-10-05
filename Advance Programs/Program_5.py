'''
# Multiprocessing Image Downloader

This program uses the multiprocessing module to download multiple images from a list of URLs in parallel. By distributing the download tasks across multiple CPU cores, it can finish the job much faster than a sequential approach, especially for a large number of images.

**Concepts:**  

Parallelism, process management, I/O-bound tasks.

**How to Run**

**1. Save the code and execute it:**

```
python Program_5.py
```
'''

import os
import requests
from multiprocessing import Pool
import time

# Create a directory to save images if it doesn't exist
SAVE_DIR = "downloaded_images"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

def download_image(url):
    """Downloads a single image from a URL and saves it."""
    try:
        print(f"Downloading: {url}")
        response = requests.get(url, timeout=15)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        # Extract filename from URL
        filename = os.path.join(SAVE_DIR, url.split("/")[-1])
        
        with open(filename, 'wb') as f:
            f.write(response.content)
        
        print(f"Finished downloading: {filename}")
        return url, "Success"
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}: {e}")
        return url, f"Failed: {e}"

if __name__ == "__main__":
    image_urls = [
        "https://images.unsplash.com/photo-1518791841217-8f162f1e1131",
        "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba",
        "https://images.unsplash.com/photo-1543852786-1cf6624b9987",
        "https://images.unsplash.com/photo-1561948955-570b270e7c36",
        "https://images.unsplash.com/photo-1574158622682-e40e6984100d"
    ]
    
    # Using a process pool to download images in parallel
    # The number of processes defaults to the number of CPU cores
    start_time = time.time()
    
    with Pool() as pool:
        results = pool.map(download_image, image_urls)
    
    end_time = time.time()
    
    print("\n--- Download Summary ---")
    for url, status in results:
        print(f"{url}: {status}")
        
    print(f"\nTotal time taken: {end_time - start_time:.2f} seconds.")