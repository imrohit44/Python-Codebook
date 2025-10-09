import os
import time
import fcntl

def tail_file_non_blocking(file_path):
    
    with open(file_path, 'r') as f:
        fd = f.fileno()
        
        # Set file descriptor to non-blocking mode
        flags = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)
        
        # Seek to end of file to only read new content
        f.seek(0, os.SEEK_END)
        
        while True:
            try:
                line = f.readline()
                if line:
                    print(line, end='')
                else:
                    # Wait briefly before checking again
                    time.sleep(0.1)
            except BlockingIOError:
                time.sleep(0.1)
            except Exception:
                return

if __name__ == '__main__':
    LOG_FILE = 'non_blocking_log.txt'
    
    # Create file
    with open(LOG_FILE, 'w') as f:
        f.write("Log started.\n")

    # Start tailing in a separate thread/process for demonstration
    import threading
    tail_thread = threading.Thread(target=tail_file_non_blocking, args=(LOG_FILE,), daemon=True)
    tail_thread.start()
    
    time.sleep(1)
    
    # Append new data from main thread
    with open(LOG_FILE, 'a') as f:
        f.write("New entry 1.\n")
        time.sleep(0.5)
        f.write("New entry 2.\n")
        time.sleep(0.5)
        
    time.sleep(2)