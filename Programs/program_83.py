import multiprocessing as mp
import time
import queue

class LockManager:
    def __init__(self):
        self.lock_status = {}
        self.request_queue = queue.Queue()
        self.running = True
    
    def run(self):
        while self.running:
            try:
                request = self.request_queue.get(timeout=1)
                action, lock_name, client_pipe = request
                
                if action == 'acquire':
                    if self.lock_status.get(lock_name) is None:
                        self.lock_status[lock_name] = client_pipe
                        client_pipe.send('granted')
                    else:
                        self.request_queue.put(request)
                
                elif action == 'release':
                    if self.lock_status.get(lock_name) == client_pipe:
                        del self.lock_status[lock_name]
                
            except queue.Empty:
                pass
    
    def stop(self):
        self.running = False

def client(manager_pipe, client_id):
    lock_name = 'shared_resource'
    
    manager_pipe.send(('acquire', lock_name, manager_pipe))
    
    while True:
        try:
            msg = manager_pipe.recv()
            if msg == 'granted':
                break
        except EOFError:
            return
            
    print(f"Client {client_id} acquired lock.")
    time.sleep(random.uniform(0.5, 1.5))
    
    print(f"Client {client_id} releasing lock.")
    manager_pipe.send(('release', lock_name, manager_pipe))
    manager_pipe.close()

if __name__ == '__main__':
    manager = LockManager()
    manager_process = mp.Process(target=manager.run)
    manager_process.daemon = True
    manager_process.start()
    
    time.sleep(1)
    
    pipes = [mp.Pipe(duplex=True) for _ in range(3)]
    clients = [mp.Process(target=client, args=(p[0], i)) for i, p in enumerate(pipes)]
    
    for c in clients:
        c.start()
    for c in clients:
        c.join()
    
    manager_process.terminate()
    manager_process.join()