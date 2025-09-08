import threading
import time
import random

# --- Simulated Database Connection and Pool ---
class MockDBConnection:
    """Simulates a database connection with transaction capabilities."""
    def __init__(self, conn_id):
        self.conn_id = conn_id
        self.in_transaction = 0 # Counter for nested transactions/savepoints
        self.is_closed = False
        self.last_used_time = time.time()
        print(f"  [DB Conn {self.conn_id}] Created.")

    def begin(self):
        self.in_transaction += 1
        if self.in_transaction == 1:
            print(f"  [DB Conn {self.conn_id}] Transaction BEGIN.")
        else:
            print(f"  [DB Conn {self.conn_id}] Transaction nested (savepoint conceptually). Current depth: {self.in_transaction}")

    def commit(self):
        if self.in_transaction == 1:
            print(f"  [DB Conn {self.conn_id}] Transaction COMMIT.")
        else:
            print(f"  [DB Conn {self.conn_id}] Inner transaction commit (no actual commit yet). Current depth: {self.in_transaction}")
        self.in_transaction = max(0, self.in_transaction - 1)

    def rollback(self):
        if self.in_transaction == 1:
            print(f"  [DB Conn {self.conn_id}] Transaction ROLLBACK!")
        else:
            print(f"  [DB Conn {self.conn_id}] Inner transaction rollback (no actual rollback yet). Current depth: {self.in_transaction}")
        self.in_transaction = max(0, self.in_transaction - 1)

    def execute(self, query):
        if self.is_closed:
            raise ConnectionError(f"Connection {self.conn_id} is closed.")
        if self.in_transaction == 0:
            print(f"  [DB Conn {self.conn_id}] Executing '{query}' (NO active transaction, might auto-commit).")
        else:
            print(f"  [DB Conn {self.conn_id}] Executing '{query}' (within transaction depth {self.in_transaction}).")
        # Simulate query execution time
        time.sleep(random.uniform(0.01, 0.05))
        return "Query Result"

    def close(self):
        if not self.is_closed:
            self.is_closed = True
            print(f"  [DB Conn {self.conn_id}] Closed.")

    def __del__(self):
        self.close() # Ensure connection is closed on object deletion

class ConnectionPool:
    """Simulates a connection pool."""
    def __init__(self, max_connections=5):
        self.max_connections = max_connections
        self.available_connections = queue.Queue(maxsize=max_connections)
        self.active_connections = set() # Track connections currently in use
        self.lock = threading.Lock() # Protect pool operations
        self.conn_id_counter = 0

        # Pre-populate pool (optional, could be lazy)
        for _ in range(max_connections):
            self.conn_id_counter += 1
            conn = MockDBConnection(self.conn_id_counter)
            self.available_connections.put(conn)

        print(f"\n[Pool] Initialized with {max_connections} connections.")

    def get_connection(self):
        """Retrieves a connection from the pool."""
        conn = None
        with self.lock:
            # Check if current thread already has an active connection associated with it
            # For "nested" transaction logic, we need to know which conn is tied to current thread.
            # This is a simplification; real pools use thread-local storage or explicit passing.
            thread_id = threading.get_ident()
            for active_conn in self.active_connections:
                if hasattr(active_conn, '_thread_owner') and active_conn._thread_owner == thread_id:
                    print(f"[Pool] Reusing existing connection {active_conn.conn_id} for thread {thread_id}.")
                    active_conn.last_used_time = time.time() # Update usage
                    return active_conn # Return existing connection for nested context
            
            # If no existing connection for this thread, get a new one
            try:
                conn = self.available_connections.get(timeout=1) # Block if no connections
                conn._thread_owner = thread_id # Mark connection as owned by this thread
                self.active_connections.add(conn)
                print(f"[Pool] Acquired connection {conn.conn_id} for thread {thread_id}. Active: {len(self.active_connections)}")
                return conn
            except queue.Empty:
                raise ConnectionError("No database connections available in the pool.")

    def release_connection(self, conn):
        """Releases a connection back to the pool."""
        with self.lock:
            if conn in self.active_connections:
                self.active_connections.remove(conn)
                # Reset transaction depth if it wasn't already (in case of unhandled error)
                conn.in_transaction = 0 
                del conn._thread_owner # Remove thread ownership
                self.available_connections.put(conn)
                print(f"[Pool] Released connection {conn.conn_id}. Available: {self.available_connections.qsize()}")
            else:
                print(f"[Pool] Warning: Attempted to release unknown connection {conn.conn_id}.")

    def shutdown(self):
        """Closes all connections in the pool."""
        print("[Pool] Shutting down...")
        while not self.available_connections.empty():
            conn = self.available_connections.get_nowait()
            conn.close()
        for conn in list(self.active_connections): # Iterate over copy as set is modified
            conn.close()
        self.active_connections.clear()
        print("[Pool] All connections closed.")


# --- Transaction Context Manager ---
class Transaction:
    _thread_local_transaction_depth = threading.local()

    def __init__(self, pool: ConnectionPool):
        self.pool = pool
        self.conn = None
        self._outermost_transaction = False # Flag for nested transaction handling

    def __enter__(self):
        # Initialize thread-local depth counter if it doesn't exist
        if not hasattr(Transaction._thread_local_transaction_depth, 'depth'):
            Transaction._thread_local_transaction_depth.depth = 0

        # Get connection if this is the outermost transaction for this thread
        if Transaction._thread_local_transaction_depth.depth == 0:
            self.conn = self.pool.get_connection()
            self._outermost_transaction = True
        else:
            # For nested transactions, reuse the existing connection
            # We assume `get_connection` handles returning the same connection
            # if already held by the current thread (as implemented in MockDBConnection).
            self.conn = self.pool.get_connection() 
            if not (hasattr(self.conn, '_thread_owner') and self.conn._thread_owner == threading.get_ident()):
                raise RuntimeError("Nested transaction tried to use a different connection, this is unexpected.")

        Transaction._thread_local_transaction_depth.depth += 1
        self.conn.begin() # Always call begin for depth tracking

        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        Transaction._thread_local_transaction_depth.depth -= 1
        
        # Only commit/rollback on the outermost transaction
        if self._outermost_transaction:
            if exc_type is None:
                self.conn.commit()
            else:
                self.conn.rollback()
                print(f"  [Transaction] Caught exception type {exc_type.__name__}, rolled back.")
            
            self.pool.release_connection(self.conn)
            self.conn = None # Clear reference
        else:
            # For inner transactions, just decrement depth, no actual commit/rollback
            if exc_type is None:
                self.conn.commit() # Simulates inner commit
            else:
                self.conn.rollback() # Simulates inner rollback
            print(f"  [Transaction] Inner transaction exiting. Depth: {Transaction._thread_local_transaction_depth.depth}")
        
        # If an exception occurred, we still let it propagate after handling the transaction
        return False # Do not suppress exceptions

# --- Simulation Functions ---
def perform_db_operations(pool, task_id):
    try:
        print(f"\n--- Task {task_id}: Starting DB operations (Success Case) ---")
        with Transaction(pool) as conn:
            conn.execute(f"INSERT INTO logs (task_id, status) VALUES ({task_id}, 'started')")
            time.sleep(random.uniform(0.1, 0.3)) # Simulate some work
            conn.execute(f"UPDATE users SET balance = balance - 10 WHERE user_id = {task_id}")
            
            # Simulate nested transaction
            print(f"  Task {task_id}: Entering nested transaction...")
            with Transaction(pool) as inner_conn:
                inner_conn.execute(f"INSERT INTO audit (action, task) VALUES ('nested_op', {task_id})")
                if random.random() < 0.1: # Small chance of inner failure
                    raise ValueError("Simulated inner transaction error!")
                inner_conn.execute(f"UPDATE analytics SET data = 'processed' WHERE id = {task_id}")
            print(f"  Task {task_id}: Exited nested transaction.")

            conn.execute(f"INSERT INTO logs (task_id, status) VALUES ({task_id}, 'completed')")
        print(f"--- Task {task_id}: Operations completed successfully ---")

    except ValueError as e:
        print(f"--- Task {task_id}: Caught error: {e}. Transaction should roll back. ---")
    except ConnectionError as e:
        print(f"--- Task {task_id}: Caught connection error: {e}. ---")
    except Exception as e:
        print(f"--- Task {task_id}: Caught unexpected error: {e}. ---")


def perform_db_operations_with_error(pool, task_id):
    try:
        print(f"\n--- Task {task_id}: Starting DB operations (Error Case) ---")
        with Transaction(pool) as conn:
            conn.execute(f"INSERT INTO logs (task_id, status) VALUES ({task_id}, 'started_error_test')")
            time.sleep(random.uniform(0.1, 0.3))
            
            if random.random() < 0.8: # High chance of error
                raise RuntimeError(f"Simulated critical error for task {task_id}!")
            
            conn.execute(f"UPDATE users SET status = 'active' WHERE user_id = {task_id}") # This should not commit
        print(f"--- Task {task_id}: Operations completed successfully (UNEXPECTED) ---")

    except RuntimeError as e:
        print(f"--- Task {task_id}: Caught expected error: {e}. Transaction should roll back. ---")
    except ConnectionError as e:
        print(f"--- Task {task_id}: Caught connection error: {e}. ---")
    except Exception as e:
        print(f"--- Task {task_id}: Caught unexpected error: {e}. ---")

if __name__ == "__main__":
    db_pool = ConnectionPool(max_connections=3) # Limit connections to observe pooling

    # Simulate multiple threads trying to use the database
    threads = []
    num_success_tasks = 3
    num_error_tasks = 2
    
    for i in range(num_success_tasks):
        t = threading.Thread(target=perform_db_operations, args=(db_pool, i + 1))
        threads.append(t)
        t.start()
        time.sleep(0.05) # Stagger thread starts slightly

    for i in range(num_error_tasks):
        t = threading.Thread(target=perform_db_operations_with_error, args=(db_pool, 100 + i + 1))
        threads.append(t)
        t.start()
        time.sleep(0.05)

    # Wait for all threads to complete
    for t in threads:
        t.join()

    print("\n--- All tasks completed. ---")
    db_pool.shutdown()