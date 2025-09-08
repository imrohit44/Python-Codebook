import threading
import time
import os
from datetime import datetime

class ThreadSafeLogger:
    _instance = None  # Singleton instance
    _lock = threading.Lock() # Lock for thread-safe file access
    
    def __new__(cls, log_file="application.log"):
        """Ensures singleton behavior."""
        with cls._lock: # Protect instance creation
            if cls._instance is None:
                cls._instance = super(ThreadSafeLogger, cls).__new__(cls)
                cls._instance._initialized = False # Flag to prevent re-initialization
                cls._instance.log_file = log_file
            return cls._instance

    def __init__(self, log_file="application.log"):
        if self._initialized: # Only initialize once
            return
        
        with self._lock: # Acquire lock before opening file
            self.log_file_path = log_file
            try:
                # Open in append mode, create if not exists
                self._file_handle = open(self.log_file_path, 'a', encoding='utf-8')
                print(f"Logger initialized. Logging to: {os.path.abspath(self.log_file_path)}")
            except IOError as e:
                print(f"Error opening log file {self.log_file_path}: {e}")
                self._file_handle = None # Indicate failure to open
            self._initialized = True

    def log(self, level: str, message: str):
        """
        Writes a timestamped log message to the file.
        """
        if not self._file_handle:
            print(f"Logger not initialized or file could not be opened. Cannot log: [{level}] {message}")
            return

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3] # Milliseconds
        log_entry = f"[{timestamp}] [{level.upper()}] {message}\n"
        
        with self._lock: # Ensure only one thread writes at a time
            try:
                self._file_handle.write(log_entry)
                self._file_handle.flush() # Ensure it's written to disk immediately
            except Exception as e:
                print(f"Error writing to log file: {e}")

    def close(self):
        """
        Closes the log file handle. Should be called when the application exits.
        """
        with self._lock:
            if self._file_handle:
                self._file_handle.close()
                self._file_handle = None
                print(f"Logger file '{self.log_file_path}' closed.")

# Simulate concurrent logging from multiple threads
def worker_function(thread_id, logger):
    for i in range(5):
        time.sleep(random.uniform(0.01, 0.1)) # Simulate some work
        level = random.choice(["INFO", "WARNING", "ERROR"])
        logger.log(level, f"Thread {thread_id}: Message {i+1}")

if __name__ == "__main__":
    LOG_FILE = "thread_safe_app.log"
    # Ensure a clean slate for the log file
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)

    # Get the logger instance (will be the same across all calls)
    logger_instance = ThreadSafeLogger(LOG_FILE)

    threads = []
    num_threads = 5
    for i in range(num_threads):
        thread = threading.Thread(target=worker_function, args=(i+1, logger_instance))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Close the logger file when all logging is done
    logger_instance.close()

    print(f"\nFinished logging. Check '{LOG_FILE}' for output.")
    # Read the log file to verify order and content
    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        print("\n--- Content of the log file ---")
        print(f.read())