import threading
import time
import random

class Rendezvous:
    def __init__(self):
        self.lock = threading.Condition()
        self.data_a = None
        self.data_b = None
        self.a_ready = threading.Event()
        self.b_ready = threading.Event()

    def exchange(self, thread_name, data):
        if thread_name == 'A':
            self.data_a = data
            self.a_ready.set()
            self.b_ready.wait()
            return self.data_b
        
        elif thread_name == 'B':
            self.data_b = data
            self.b_ready.set()
            self.a_ready.wait()
            return self.data_a

def thread_a_func(rendezvous):
    print("Thread A: Starting preliminary work.")
    time.sleep(random.uniform(0.5, 1.0))
    data_to_send = "Message from A"
    
    received_data = rendezvous.exchange('A', data_to_send)
    
    print(f"Thread A: Final work started. Received: {received_data}")
    time.sleep(0.5)

def thread_b_func(rendezvous):
    print("Thread B: Starting preliminary work.")
    time.sleep(random.uniform(0.5, 1.0))
    data_to_send = "Message from B"
    
    received_data = rendezvous.exchange('B', data_to_send)
    
    print(f"Thread B: Final work started. Received: {received_data}")
    time.sleep(0.5)

if __name__ == '__main__':
    rv = Rendezvous()
    
    t_a = threading.Thread(target=thread_a_func, args=(rv,))
    t_b = threading.Thread(target=thread_b_func, args=(rv,))
    
    t_a.start()
    t_b.start()
    
    t_a.join()
    t_b.join()