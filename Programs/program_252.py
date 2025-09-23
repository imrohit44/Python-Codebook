import threading
import queue
import time
import os
import gzip

def process_and_compress(file_path, output_path):
    with open(file_path, 'r') as f_in:
        content = f_in.read().upper()
    
    with gzip.open(output_path, 'wb') as f_out:
        f_out.write(content.encode('utf-8'))

def worker(q, input_dir, output_dir):
    while True:
        try:
            file_name = q.get(timeout=1)
            file_path = os.path.join(input_dir, file_name)
            output_path = os.path.join(output_dir, f"{file_name}.gz")
            process_and_compress(file_path, output_path)
            q.task_done()
        except queue.Empty:
            break

def master(file_paths, num_threads, input_dir, output_dir):
    q = queue.Queue()
    for path in file_paths:
        q.put(path)
    
    threads = [threading.Thread(target=worker, args=(q, input_dir, output_dir)) for _ in range(num_threads)]
    
    for t in threads:
        t.start()
    
    q.join()
    
    for t in threads:
        t.join()

if __name__ == '__main__':
    input_dir = 'logs'
    output_dir = 'compressed_logs'
    
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    for i in range(10):
        with open(os.path.join(input_dir, f"log_{i}.txt"), 'w') as f:
            f.write("This is a log message.\n")
    
    file_list = [f"log_{i}.txt" for i in range(10)]
    master(file_list, num_threads=4, input_dir=input_dir, output_dir=output_dir)