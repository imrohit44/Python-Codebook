import mmap
import multiprocessing as mp
import os
import struct
import time

def sender(shm_name, file_path):
    with open(file_path, 'rb') as f:
        data = f.read()
    
    shm = mp.shared_memory.SharedMemory(shm_name)
    shm_size = len(data)
    
    shm.buf[0:4] = struct.pack('<I', shm_size)
    shm.buf[4:4 + shm_size] = data
    
    shm.close()

def receiver(shm_name, output_path):
    shm = mp.shared_memory.SharedMemory(shm_name)
    
    while shm.buf[0] == 0:
        time.sleep(0.01)
        
    shm_size = struct.unpack('<I', shm.buf[0:4])[0]
    data = shm.buf[4:4 + shm_size]
    
    with open(output_path, 'wb') as f:
        f.write(data)
        
    shm.close()

if __name__ == '__main__':
    FILE_SIZE = 1024 * 1024
    FILE_IN = 'input_file.bin'
    FILE_OUT = 'output_file.bin'
    SHM_NAME = 'zero_copy_test'
    
    with open(FILE_IN, 'wb') as f:
        f.write(os.urandom(FILE_SIZE))

    shm = mp.shared_memory.SharedMemory(create=True, size=FILE_SIZE + 4, name=SHM_NAME)
    
    p_sender = mp.Process(target=sender, args=(SHM_NAME, FILE_IN))
    p_receiver = mp.Process(target=receiver, args=(SHM_NAME, FILE_OUT))
    
    p_sender.start()
    p_receiver.start()
    
    p_sender.join()
    p_receiver.join()
    
    shm.close()
    shm.unlink()
    os.remove(FILE_IN)
    os.remove(FILE_OUT)