import socket
import threading
import queue
import pickle
import time
import random

# --- Constants ---
BROKER_HOST = '127.0.0.1'
BROKER_PORT = 12345
TASK_REQUEST = "GET_TASK"
TASK_SUBMIT = "SUBMIT_TASK"
TASK_DONE = "TASK_DONE"
NO_TASK = "NO_TASK"
BUFFER_SIZE = 4096

# --- Task Definition (for serialization) ---
class Task:
    def __init__(self, task_id, func_name, args=None, kwargs=None):
        self.task_id = task_id
        self.func_name = func_name
        self.args = args if args is not None else ()
        self.kwargs = kwargs if kwargs is not None else {}
        self.status = "PENDING"
        self.result = None

    def __repr__(self):
        return f"Task(id={self.task_id}, func={self.func_name}, status={self.status})"

# --- Broker Implementation ---
class Broker:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.task_queue = queue.Queue() # Thread-safe queue for tasks
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = [] # To keep track of connected sockets
        self.running = True
        self.task_id_counter = 0
        self.lock = threading.Lock() # For task_id_counter and client list

    def _generate_task_id(self):
        with self.lock:
            self.task_id_counter += 1
            return self.task_id_counter

    def _handle_client(self, conn, addr):
        print(f"[Broker] New connection from {addr}")
        try:
            while self.running:
                data = conn.recv(BUFFER_SIZE)
                if not data:
                    break # Client disconnected
                
                try:
                    message = pickle.loads(data)
                except pickle.UnpicklingError:
                    print(f"[Broker] Invalid message from {addr}: {data[:50]}...")
                    continue # Skip invalid message
                
                msg_type = message.get("type")

                if msg_type == TASK_SUBMIT:
                    task_info = message.get("task")
                    if task_info:
                        task = Task(self._generate_task_id(), task_info['func_name'], task_info['args'], task_info['kwargs'])
                        self.task_queue.put(task)
                        print(f"[Broker] Received task {task.task_id} from producer {addr}. Queue size: {self.task_queue.qsize()}")
                        conn.sendall(pickle.dumps({"status": "SUCCESS", "task_id": task.task_id}))
                    else:
                        conn.sendall(pickle.dumps({"status": "ERROR", "message": "No task info provided."}))

                elif msg_type == TASK_REQUEST:
                    try:
                        task = self.task_queue.get_nowait()
                        print(f"[Broker] Worker {addr} requested task. Sending task {task.task_id}. Queue size: {self.task_queue.qsize()}")
                        conn.sendall(pickle.dumps({"type": TASK_REQUEST, "task": task}))
                    except queue.Empty:
                        # print(f"[Broker] No tasks for worker {addr}. Queue empty.")
                        conn.sendall(pickle.dumps({"type": NO_TASK}))
                    
                elif msg_type == TASK_DONE:
                    task_id = message.get("task_id")
                    result = message.get("result")
                    print(f"[Broker] Task {task_id} completed by worker {addr} with result: {result}")
                    # In a real system, broker would store results or notify producer
                    conn.sendall(pickle.dumps({"status": "ACK_TASK_DONE"}))

                else:
                    print(f"[Broker] Unknown message type from {addr}: {msg_type}")
                    conn.sendall(pickle.dumps({"status": "ERROR", "message": "Unknown message type."}))

        except Exception as e:
            print(f"[Broker] Error handling client {addr}: {e}")
        finally:
            with self.lock:
                if conn in self.clients:
                    self.clients.remove(conn)
            conn.close()
            print(f"[Broker] Client {addr} disconnected.")

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"[Broker] Broker listening on {self.host}:{self.port}")
        
        accept_thread = threading.Thread(target=self._accept_connections, daemon=True)
        accept_thread.start()

    def _accept_connections(self):
        while self.running:
            try:
                self.server_socket.settimeout(1.0) # Allows graceful shutdown
                conn, addr = self.server_socket.accept()
                with self.lock:
                    self.clients.append(conn)
                threading.Thread(target=self._handle_client, args=(conn, addr), daemon=True).start()
            except socket.timeout:
                continue
            except Exception as e:
                if self.running:
                    print(f"[Broker] Error accepting connections: {e}")
                break
        print("[Broker] Broker accept loop stopped.")

    def stop(self):
        print("[Broker] Shutting down Broker...")
        self.running = False
        with self.lock:
            for client_conn in self.clients:
                try:
                    client_conn.shutdown(socket.SHUT_RDWR)
                    client_conn.close()
                except Exception:
                    pass
            self.clients.clear()
        try:
            self.server_socket.shutdown(socket.SHUT_RDWR)
            self.server_socket.close()
        except Exception:
            pass
        print("[Broker] Broker stopped.")

# --- Worker Implementation ---
class Worker:
    def __init__(self, broker_host, broker_port, worker_id, known_funcs):
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.worker_id = worker_id
        self.known_funcs = known_funcs
        self.socket = None
        self.running = True

    def _connect(self):
        if self.socket:
            try: self.socket.close()
            except: pass
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((self.broker_host, self.broker_port))
            print(f"[Worker {self.worker_id}] Connected to broker.")
            return True
        except socket.error as e:
            print(f"[Worker {self.worker_id}] Could not connect to broker: {e}. Retrying...")
            return False

    def start(self):
        while self.running:
            if not self._connect():
                time.sleep(2) # Wait before retrying connection
                continue

            try:
                # Request a task
                self.socket.sendall(pickle.dumps({"type": TASK_REQUEST}))
                response_data = self.socket.recv(BUFFER_SIZE)
                response = pickle.loads(response_data)

                if response.get("type") == TASK_REQUEST and response.get("task"):
                    task = response["task"]
                    print(f"[Worker {self.worker_id}] Received task {task.task_id}: {task.func_name}")
                    
                    if task.func_name in self.known_funcs:
                        try:
                            func = self.known_funcs[task.func_name]
                            # Simulate work
                            time.sleep(random.uniform(0.5, 2.0))
                            result = func(*task.args, **task.kwargs)
                            print(f"[Worker {self.worker_id}] Task {task.task_id} completed. Result: {result}")
                            self.socket.sendall(pickle.dumps({"type": TASK_DONE, "task_id": task.task_id, "result": result}))
                            ack = pickle.loads(self.socket.recv(BUFFER_SIZE))
                            # print(f"[Worker {self.worker_id}] Broker ACK: {ack}")
                        except Exception as e:
                            print(f"[Worker {self.worker_id}] Error executing task {task.task_id}: {e}")
                            self.socket.sendall(pickle.dumps({"type": TASK_DONE, "task_id": task.task_id, "result": f"ERROR: {e}"}))
                            pickle.loads(self.socket.recv(BUFFER_SIZE)) # consume ACK
                    else:
                        print(f"[Worker {self.worker_id}] Unknown function '{task.func_name}' for task {task.task_id}")
                        self.socket.sendall(pickle.dumps({"type": TASK_DONE, "task_id": task.task_id, "result": f"ERROR: Unknown function {task.func_name}"}))
                        pickle.loads(self.socket.recv(BUFFER_SIZE)) # consume ACK
                elif response.get("type") == NO_TASK:
                    # print(f"[Worker {self.worker_id}] No tasks available. Waiting...")
                    time.sleep(1) # Wait before asking again
                else:
                    print(f"[Worker {self.worker_id}] Unexpected response from broker: {response}")

            except (socket.error, ConnectionResetError, pickle.UnpicklingError) as e:
                print(f"[Worker {self.worker_id}] Connection error: {e}. Reconnecting...")
                self._connect() # Attempt to reconnect
                time.sleep(1)
            except Exception as e:
                print(f"[Worker {self.worker_id}] Unexpected error: {e}")
                self.stop() # Critical error, stop worker

    def stop(self):
        print(f"[Worker {self.worker_id}] Shutting down worker...")
        self.running = False
        if self.socket:
            try:
                self.socket.shutdown(socket.SHUT_RDWR)
                self.socket.close()
            except Exception:
                pass
        print(f"[Worker {self.worker_id}] Worker stopped.")

# --- Producer Implementation ---
class Producer:
    def __init__(self, broker_host, broker_port, producer_id):
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.producer_id = producer_id
        self.socket = None
        self.running = True

    def _connect(self):
        if self.socket:
            try: self.socket.close()
            except: pass
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((self.broker_host, self.broker_port))
            print(f"[Producer {self.producer_id}] Connected to broker.")
            return True
        except socket.error as e:
            print(f"[Producer {self.producer_id}] Could not connect to broker: {e}. Retrying...")
            return False

    def submit_task(self, func_name, *args, **kwargs):
        if not self._connect():
            print(f"[Producer {self.producer_id}] Failed to connect to broker, cannot submit task.")
            return None

        task_payload = {
            "func_name": func_name,
            "args": args,
            "kwargs": kwargs
        }
        message = {"type": TASK_SUBMIT, "task": task_payload}
        try:
            self.socket.sendall(pickle.dumps(message))
            response_data = self.socket.recv(BUFFER_SIZE)
            response = pickle.loads(response_data)
            if response.get("status") == "SUCCESS":
                print(f"[Producer {self.producer_id}] Task '{func_name}' submitted successfully, ID: {response.get('task_id')}")
                return response.get('task_id')
            else:
                print(f"[Producer {self.producer_id}] Failed to submit task: {response.get('message')}")
                return None
        except (socket.error, ConnectionResetError, pickle.UnpicklingError) as e:
            print(f"[Producer {self.producer_id}] Connection error during submission: {e}. Retrying...")
            self._connect() # Attempt to reconnect for next task
            return None
        except Exception as e:
            print(f"[Producer {self.producer_id}] Unexpected error submitting task: {e}")
            return None
        finally:
            if self.socket: # Close connection after each submission for simplicity in this example
                try:
                    self.socket.close()
                except Exception:
                    pass
                self.socket = None


    def stop(self):
        print(f"[Producer {self.producer_id}] Shutting down producer...")
        self.running = False
        if self.socket:
            try:
                self.socket.close()
            except Exception:
                pass
        print(f"[Producer {self.producer_id}] Producer stopped.")

# --- Functions for Workers to execute ---
def simple_add(a, b):
    return a + b

def complex_calc(n_iterations):
    result = 0
    for i in range(n_iterations):
        result += i * random.random()
    return f"Calc done: {round(result, 2)}"

def greet_name(name="World"):
    return f"Hello, {name}!"

# --- Main Simulation ---
if __name__ == "__main__":
    # Start Broker in a separate thread
    broker = Broker(BROKER_HOST, BROKER_PORT)
    broker_thread = threading.Thread(target=broker.start, daemon=True)
    broker_thread.start()
    time.sleep(1) # Give broker time to start up

    # Start Workers
    worker_functions = {
        "simple_add": simple_add,
        "complex_calc": complex_calc,
        "greet_name": greet_name
    }
    num_workers = 3
    workers = []
    worker_threads = []
    for i in range(num_workers):
        worker = Worker(BROKER_HOST, BROKER_PORT, i + 1, worker_functions)
        workers.append(worker)
        w_thread = threading.Thread(target=worker.start, daemon=True)
        worker_threads.append(w_thread)
        w_thread.start()
    time.sleep(1) # Give workers time to connect

    # Start Producers
    num_producers = 2
    producers = []
    for i in range(num_producers):
        producers.append(Producer(BROKER_HOST, BROKER_PORT, i + 1))

    # Submit some tasks
    print("\n--- Submitting Tasks ---")
    producers[0].submit_task("simple_add", 10, 20)
    producers[1].submit_task("greet_name", name="Alice")
    producers[0].submit_task("complex_calc", n_iterations=1000000)
    producers[1].submit_task("simple_add", 5, 8)
    producers[0].submit_task("greet_name")
    producers[1].submit_task("complex_calc", n_iterations=500000)
    producers[0].submit_task("non_existent_func") # Test unknown function

    # Let the system run for a while
    print("\n--- Allowing system to run for 10 seconds ---")
    time.sleep(10)

    # Clean up (join non-daemon threads if any, or just let daemons exit with main)
    # For this example, we're using daemon threads, so they'll exit when the main thread exits.
    # To ensure graceful shutdown, you'd call .stop() on each instance and then .join() on its thread.
    print("\n--- Shutting down simulation ---")
    for w in workers:
        w.stop()
    for p in producers:
        p.stop()
    broker.stop()
    
    # Give threads a moment to finish their cleanup
    time.sleep(1) 
    print("Simulation finished.")