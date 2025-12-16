import queue
import threading
import time

class Connection:
    """Simulates an expensive-to-create resource."""
    def __init__(self, id):
        self.id = id
        print(f"Connection {id} created.")
        self.is_open = True
    
    def execute(self, query):
        time.sleep(0.05)
        return f"Conn {self.id}: Executed '{query}'"
    
    def close(self):
        self.is_open = False
        print(f"Connection {self.id} closed.")

class ObjectPool:
    def __init__(self, size, resource_factory):
        self.pool = queue.Queue(size)
        for i in range(size):
            self.pool.put(resource_factory(i))

    def borrow(self):
        return self.pool.get()

    def release(self, resource):
        self.pool.put(resource)
        
def task_worker(pool, thread_id):
    conn = None
    try:
        conn = pool.borrow()
        result = conn.execute(f"SELECT data for Thread {thread_id}")
        print(f"Thread {thread_id}: {result}")
    finally:
        if conn:
            pool.release(conn)

if __name__ == '__main__':
    pool_size = 3
    db_pool = ObjectPool(pool_size, Connection)
    
    threads = [threading.Thread(target=task_worker, args=(db_pool, i)) for i in range(5)]
    
    for t in threads:
        t.start()
    for t in threads:
        t.join()