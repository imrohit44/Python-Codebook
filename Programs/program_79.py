import threading
import queue
import time
import os

def process_file(file_path):
    time.sleep(0.1)
    if 'error' in file_path:
        raise ValueError(f"Simulated error for {file_path}")
    with open(file_path, 'r') as f:
        content = f.read()
    return f"Processed {file_path} with length {len(content)}"

def worker(task_queue, result_queue):
    while True:
        try:
            file_path = task_queue.get(timeout=1)
            try:
                result = process_file(file_path)
                result_queue.put(('success', result))
            except Exception as e:
                result_queue.put(('error', str(e)))
            finally:
                task_queue.task_done()
        except queue.Empty:
            break

def master(file_paths, num_threads):
    task_queue = queue.Queue()
    result_queue = queue.Queue()
    
    for path in file_paths:
        task_queue.put(path)
    
    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=worker, args=(task_queue, result_queue))
        threads.append(t)
        t.start()
        
    task_queue.join()
    
    successes, failures = [], []
    while not result_queue.empty():
        status, message = result_queue.get()
        if status == 'success':
            successes.append(message)
        else:
            failures.append(message)
            
    return successes, failures

if __name__ == '__main__':
    temp_dir = "temp_files"
    os.makedirs(temp_dir, exist_ok=True)
    
    file_paths = []
    for i in range(10):
        file_path = os.path.join(temp_dir, f"file_{i}.txt")
        with open(file_path, 'w') as f:
            f.write("a" * (i + 1) * 10)
        file_paths.append(file_path)
    file_paths.append(os.path.join(temp_dir, "error_file.txt"))
    
    successes, failures = master(file_paths, num_threads=4)
    
    print("--- Summary ---")
    print(f"Successes: {len(successes)}")
    for s in successes:
        print(f"  - {s}")
    print(f"Failures: {len(failures)}")
    for f in failures:
        print(f"  - {f}")