import threading
import queue
import time
import os

class LogManager:
    def __init__(self, filename, max_size):
        self.filename = filename
        self.max_size = max_size
        self.log_queue = queue.Queue()
        self.lock = threading.Lock()
        self.running = True
        self.writer_thread = threading.Thread(target=self._writer, daemon=True)
        self.writer_thread.start()

    def _writer(self):
        file_index = 0
        while self.running:
            try:
                log_entry = self.log_queue.get(timeout=0.1)
                
                with self.lock:
                    log_file = self.filename if file_index == 0 else f"{self.filename}.{file_index}"
                    
                    if os.path.exists(log_file) and os.path.getsize(log_file) > self.max_size:
                        file_index += 1
                        log_file = f"{self.filename}.{file_index}"
                    
                    with open(log_file, 'a') as f:
                        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {log_entry}\n")
                        
                self.log_queue.task_done()
            except queue.Empty:
                continue

    def log(self, message):
        self.log_queue.put(message)

    def stop(self):
        self.running = False
        self.writer_thread.join()

def worker(log_manager, thread_id):
    for i in range(10):
        log_manager.log(f"Thread {thread_id}: Log message {i}")
        time.sleep(0.01)

if __name__ == "__main__":
    log_manager = LogManager('app.log', max_size=1024)
    
    threads = []
    for i in range(5):
        t = threading.Thread(target=worker, args=(log_manager, i))
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
    log_manager.stop()