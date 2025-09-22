import threading
import queue
import time
from collections import defaultdict

class MessageBroker:
    def __init__(self):
        self.topics = defaultdict(list)
        self.messages = queue.Queue()
        self.lock = threading.Lock()
        self.running = True
        self.worker = threading.Thread(target=self._run)
        self.worker.start()

    def subscribe(self, topic, subscriber_queue):
        with self.lock:
            self.topics[topic].append(subscriber_queue)

    def publish(self, topic, message):
        self.messages.put((topic, message))

    def _run(self):
        while self.running:
            try:
                topic, message = self.messages.get(timeout=1)
                subscribers = self.topics.get(topic, [])
                for q in subscribers:
                    q.put(message)
                self.messages.task_done()
            except queue.Empty:
                continue

    def stop(self):
        self.running = False
        self.worker.join()

def subscriber(broker, topic, id):
    q = queue.Queue()
    broker.subscribe(topic, q)
    while True:
        try:
            message = q.get(timeout=1)
            print(f"Subscriber {id} on topic '{topic}': {message}")
        except queue.Empty:
            return

def publisher(broker, topic, num_messages):
    for i in range(num_messages):
        broker.publish(topic, f"Message {i} from publisher")
        time.sleep(0.5)

if __name__ == '__main__':
    broker = MessageBroker()
    
    sub1_q = queue.Queue()
    sub2_q = queue.Queue()
    
    sub1_thread = threading.Thread(target=subscriber, args=(broker, 'news', 1))
    sub2_thread = threading.Thread(target=subscriber, args=(broker, 'news', 2))
    pub_thread = threading.Thread(target=publisher, args=(broker, 'news', 5))
    
    sub1_thread.start()
    sub2_thread.start()
    pub_thread.start()
    
    pub_thread.join()
    
    broker.stop()