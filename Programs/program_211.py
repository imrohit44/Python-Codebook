import os
import selectors
import time

def read_file_non_blocking(file_path):
    with open(file_path, 'rb') as f:
        fd = f.fileno()
        
        flags = os.O_NONBLOCK
        os.set_blocking(fd, False)
        
        sel = selectors.DefaultSelector()
        sel.register(fd, selectors.EVENT_READ)
        
        full_data = bytearray()
        
        while True:
            events = sel.select(timeout=1)
            if not events:
                break
                
            for key, mask in events:
                data = os.read(key.fd, 1024)
                if not data:
                    return full_data
                full_data.extend(data)
                
    return full_data

if __name__ == '__main__':
    with open('test_file.txt', 'w') as f:
        f.write("This is a test file for non-blocking I/O.")
        
    data = read_file_non_blocking('test_file.txt')
    print(f"Read data: {data.decode()}")
    
    os.remove('test_file.txt')