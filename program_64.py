import threading
import queue
import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin, urlparse

class WebCrawler:
    def __init__(self, start_url, num_threads):
        self.queue = queue.Queue()
        self.queue.put(start_url)
        self.visited = set()
        self.visited_lock = threading.Lock()
        self.num_threads = num_threads
        self.workers = []

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
                try:
                    response = requests.get(url, timeout=5)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    for link in soup.find_all('a'):
                        href = link.get('href')
                        if href:
                            absolute_url = urljoin(url, href)
                            if urlparse(absolute_url).netloc == urlparse(url).netloc:
                                with self.visited_lock:
                                    if absolute_url not in self.visited:
                                        self.queue.put(absolute_url)
                except requests.exceptions.RequestException as e:
                    print(f"Failed to fetch {url}: {e}")
                finally:
                    self.queue.task_done()
            except queue.Empty:
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                self.queue.task_done()

    def start(self):
        for _ in range(self.num_threads):
            worker_thread = threading.Thread(target=self._worker, daemon=True)
            self.workers.append(worker_thread)
            worker_thread.start()
        
        self.queue.join()
        print("\nCrawler finished.")

if __name__ == "__main__":
    crawler = WebCrawler("https://example.com", num_threads=4)
    crawler.start()