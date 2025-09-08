import threading
import time

class MockDBConnection:
    def __init__(self, conn_id):
        self.conn_id = conn_id
        self.in_transaction_count = 0
        self.savepoints = []

    def begin(self):
        self.in_transaction_count += 1
        if self.in_transaction_count > 1:
            savepoint_name = f"sp{len(self.savepoints) + 1}"
            self.savepoints.append(savepoint_name)
            print(f"  [DB Conn {self.conn_id}] Savepoint set: {savepoint_name}")
        else:
            print(f"  [DB Conn {self.conn_id}] Transaction begun.")

    def commit(self):
        if self.savepoints:
            self.savepoints.pop()
            print(f"  [DB Conn {self.conn_id}] Releasing savepoint.")
        else:
            print(f"  [DB Conn {self.conn_id}] Transaction committed.")
        self.in_transaction_count -= 1

    def rollback(self):
        if self.savepoints:
            savepoint_name = self.savepoints.pop()
            print(f"  [DB Conn {self.conn_id}] Rolling back to savepoint: {savepoint_name}")
        else:
            print(f"  [DB Conn {self.conn_id}] Transaction rolled back!")
        self.in_transaction_count -= 1

class Transaction:
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def __enter__(self):
        self.db_conn.begin()
        return self.db_conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.db_conn.commit()
        else:
            self.db_conn.rollback()

        return False

def task_with_nested_transactions(conn):
    with Transaction(conn):
        print("  Outer transaction entered.")
        conn.execute("UPDATE A")

        try:
            with Transaction(conn):
                print("  Inner transaction entered.")
                conn.execute("UPDATE B")
                if random.random() > 0.5:
                    raise ValueError("Simulated error in inner transaction.")
                conn.execute("UPDATE C")
            print("  Inner transaction committed.")
        except ValueError as e:
            print(f"  Caught: {e}. Inner transaction rolled back.")

        conn.execute("UPDATE D")
    print("  Outer transaction committed.")

if __name__ == "__main__":
    conn = MockDBConnection(1)
    task_with_nested_transactions(conn)