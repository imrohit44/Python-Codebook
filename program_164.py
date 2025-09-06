import threading
import queue
import time
import os
import gzip

class LogManager:
    def __init__(self, filename, max_size, max_log_files):
        self.filename = filename
        self.max_size = max_size
        self.max_log_files = max_log_files
        self.log_queue = queue.Queue()
        self.lock = threading.Lock()
        self.running = True
        self.writer_thread = threading.Thread(target=self._writer, daemon=True)
        self.writer_thread.start()

    def _rotate_logs(self, current_log_file):
        for i in range(self.max_log_files - 1, 0, -1):
            source = f"{self.filename}.{i}.gz"
            dest = f"{self.filename}.{i+1}.gz"
            if os.path.exists(source):
                os.rename(source, dest)
        
        with open(current_log_file, 'rb') as f_in:
            with gzip.open(f"{self.filename}.1.gz", 'wb') as f_out:
                f_out.writelines(f_in)
        os.remove(current_log_file)

    def _writer(self):
        current_log_file = self.filename
        while self.running:
            try:
                log_entry = self.log_queue.get(timeout=0.1)
                
                with self.lock:
                    if os.path.exists(current_log_file) and os.path.getsize(current_log_file) > self.max_size:
                        self._rotate_logs(current_log_file)
                    
                    with open(current_log_file, 'a') as f:
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
    for i in range(100):
        log_manager.log(f"Thread {thread_id}: Log message {i}")
        time.sleep(0.01)

if __name__ == '__main__':
    log_manager = LogManager('app.log', max_size=1024 * 10, max_log_files=5)
    
    threads = [threading.Thread(target=worker, args=(log_manager, i)) for i in range(5)]
    
    for t in threads:
        t.start()
        
    for t in threads:
        t.join()
        
    log_manager.stop()