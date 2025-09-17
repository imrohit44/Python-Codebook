import threading
import time

class FileSystem:
    def __init__(self):
        self.root = {}
        self.lock = threading.Lock()

    def create_file(self, path, content):
        with self.lock:
            parts = path.strip('/').split('/')
            current_dir = self.root
            for part in parts[:-1]:
                if part not in current_dir or not isinstance(current_dir[part], dict):
                    current_dir[part] = {}
                current_dir = current_dir[part]
            current_dir[parts[-1]] = content
            
    def read_file(self, path):
        with self.lock:
            parts = path.strip('/').split('/')
            current_dir = self.root
            for part in parts[:-1]:
                if part not in current_dir or not isinstance(current_dir[part], dict):
                    return None
                current_dir = current_dir[part]
            return current_dir.get(parts[-1])
            
    def list_dir(self, path):
        with self.lock:
            parts = path.strip('/').split('/')
            current_dir = self.root
            for part in parts:
                if part not in current_dir or not isinstance(current_dir[part], dict):
                    return None
                current_dir = current_dir[part]
            return list(current_dir.keys())

def worker(fs, worker_id):
    fs.create_file(f"dir{worker_id}/file1.txt", f"Content from worker {worker_id}")
    time.sleep(0.1)
    fs.read_file(f"dir{worker_id}/file1.txt")

if __name__ == '__main__':
    fs = FileSystem()
    threads = [threading.Thread(target=worker, args=(fs, i)) for i in range(5)]
    
    for t in threads:
        t.start()
    for t in threads:
        t.join()
        
    print(fs.list_dir('/'))
    print(fs.read_file('dir0/file1.txt'))