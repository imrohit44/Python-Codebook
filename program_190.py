import threading
import queue
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from collections import OrderedDict
import time

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()
        self.lock = threading.Lock()

    def get(self, key):
        with self.lock:
            if key in self.cache:
                value = self.cache.pop(key)
                self.cache[key] = value
                return value
            return None

    def put(self, key, value):
        with self.lock:
            if key in self.cache:
                self.cache.pop(key)
            elif len(self.cache) >= self.capacity:
                self.cache.popitem(last=False)
            self.cache[key] = value

class WebCrawler:
    def __init__(self, start_url, num_threads, cache_capacity):
        self.queue = queue.Queue()
        self.queue.put(start_url)
        self.visited = set()
        self.visited_lock = threading.Lock()
        self.num_threads = num_threads
        self.workers = []
        self.cache = LRUCache(cache_capacity)
        
    def _worker(self):
        while True:
            try:
                url = self.queue.get(timeout=1)
                
                with self.visited_lock:
                    if url in self.visited:
                        self.queue.task_done()
                        continue
                    self.visited.add(url)
                
                print(f"Crawling: {url}")
                
                cached_page = self.cache.get(url)
                if cached_page:
                    print(f"  - Using cached page for {url}")
                    soup = BeautifulSoup(cached_page, 'html.parser')
                else:
                    try:
                        response = requests.get(url, timeout=5)
                        soup = BeautifulSoup(response.text, 'html.parser')
                        self.cache.put(url, response.text)
                    except requests.exceptions.RequestException as e:
                        print(f"  - Failed to fetch {url}: {e}")
                        self.queue.task_done()
                        continue
                
                for link in soup.find_all('a'):
                    href = link.get('href')
                    if href:
                        absolute_url = urljoin(url, href)
                        if urlparse(absolute_url).netloc == urlparse(url).netloc:
                            with self.visited_lock:
                                if absolute_url not in self.visited:
                                    self.queue.put(absolute_url)
                
                self.queue.task_done()
            except queue.Empty:
                break
            except Exception as e:
                print(f"  - An error occurred: {e}")
                self.queue.task_done()

    def start(self):
        for _ in range(self.num_threads):
            worker_thread = threading.Thread(target=self._worker, daemon=True)
            self.workers.append(worker_thread)
            worker_thread.start()
        
        self.queue.join()
        print("\nCrawler finished.")

if __name__ == "__main__":
    crawler = WebCrawler("https://example.com", num_threads=4, cache_capacity=10)
    crawler.start()