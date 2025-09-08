import multiprocessing as mp
import numpy as np
import time
import threading

def producer(shm_in, count):
    np_array = np.ndarray((count,), dtype=np.int32, buffer=shm_in.buf)
    for i in range(count):
        np_array[i] = i
        time.sleep(0.01)

def consumer(shm_in, shm_out, process_id, lock_in, lock_out):
    while True:
        with lock_in:
            data = np.ndarray((1,), dtype=np.int32, buffer=shm_in.buf)
            if data[0] == -1:
                with lock_out:
                    out_array = np.ndarray((1,), dtype=np.int32, buffer=shm_out.buf)
                    out_array[0] = -1
                break
            
            result = data[0] * 2
            data[0] = -1

        with lock_out:
            out_array = np.ndarray((1,), dtype=np.int32, buffer=shm_out.buf)
            out_array[0] = result
        
        time.sleep(0.01)

if __name__ == '__main__':
    count = 10
    
    shm_in = mp.shared_memory.SharedMemory(create=True, size=np.dtype(np.int32).itemsize)
    shm_out = mp.shared_memory.SharedMemory(create=True, size=np.dtype(np.int32).itemsize)
    
    lock_in = mp.Lock()
    lock_out = mp.Lock()
    
    producer_process = mp.Process(target=producer, args=(shm_in, count))
    consumers = [mp.Process(target=consumer, args=(shm_in, shm_out, i, lock_in, lock_out)) for i in range(2)]
    
    producer_process.start()
    [c.start() for c in consumers]
    
    producer_process.join()
    
    print("Producer finished.")
    
    np_out = np.ndarray((count,), dtype=np.int32, buffer=shm_out.buf)
    for _ in range(count):
        while True:
            with lock_out:
                result = np_out[0]
                if result != -1:
                    print(f"Result: {result}")
                    np_out[0] = -1
                    break
        
    shm_in.close()
    shm_in.unlink()
    shm_out.close()
    shm_out.unlink()