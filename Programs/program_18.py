import time
import random
import threading
import queue

class Producer(threading.Thread):
    def __init__(self, queue_obj, producer_id, num_messages=5):
        super().__init__()
        self.queue = queue_obj
        self.producer_id = producer_id
        self.num_messages = num_messages
        self.stop_event = threading.Event() # For graceful shutdown

    def run(self):
        print(f"Producer {self.producer_id}: Starting...")
        for i in range(self.num_messages):
            if self.stop_event.is_set():
                break
            
            message_data = {
                "producer_id": self.producer_id,
                "message_id": i + 1,
                "timestamp": time.time(),
                "content": f"Data from Producer {self.producer_id}, Msg {i+1}"
            }
            try:
                self.queue.put(message_data, timeout=1) # Add timeout to prevent blocking indefinitely
                print(f"Producer {self.producer_id}: Put message {i+1}")
            except queue.Full:
                print(f"Producer {self.producer_id}: Queue is full, retrying...")
                time.sleep(0.1) # Wait a bit before retrying
            
            time.sleep(random.uniform(0.1, 0.5)) # Simulate work before next message
        print(f"Producer {self.producer_id}: Finished producing messages.")

    def stop(self):
        self.stop_event.set()

class Consumer(threading.Thread):
    def __init__(self, queue_obj, consumer_id):
        super().__init__()
        self.queue = queue_obj
        self.consumer_id = consumer_id
        self.stop_event = threading.Event() # For graceful shutdown

    def run(self):
        print(f"Consumer {self.consumer_id}: Starting...")
        while not self.stop_event.is_set() or not self.queue.empty():
            try:
                message = self.queue.get(timeout=0.5) # Add timeout to prevent blocking indefinitely
                self._process_message(message)
                self.queue.task_done() # Indicate that the task for this message is done
            except queue.Empty:
                if self.stop_event.is_set():
                    # If stop event is set and queue is empty, exit
                    break
                # print(f"Consumer {self.consumer_id}: Queue is empty, waiting...")
                time.sleep(0.1) # Wait a bit before checking again
            except Exception as e:
                print(f"Consumer {self.consumer_id}: Error processing message: {e}")
                
        print(f"Consumer {self.consumer_id}: Shutting down.")

    def _process_message(self, message):
        """Simulate processing the message."""
        processing_time = random.uniform(0.2, 1.0)
        # print(f"Consumer {self.consumer_id}: Processing message from P{message['producer_id']}, Msg {message['message_id']}...")
        time.sleep(processing_time) # Simulate work
        print(f"Consumer {self.consumer_id}: Processed Msg {message['message_id']} from P{message['producer_id']} in {processing_time:.2f}s.")

    def stop(self):
        self.stop_event.set()

# Main script
if __name__ == "__main__":
    message_queue = queue.Queue(maxsize=10) # Bounded queue

    num_producers = 3
    num_consumers = 2
    total_messages_per_producer = 5

    producers = [Producer(message_queue, i + 1, total_messages_per_producer) for i in range(num_producers)]
    consumers = [Consumer(message_queue, i + 1) for i in range(num_consumers)]

    # Start producers and consumers
    for p in producers:
        p.start()
    for c in consumers:
        c.start()

    # Wait for all producers to finish their work
    for p in producers:
        p.join()
    print("\nAll producers have finished sending messages.")

    # Signal consumers to stop once all messages are processed
    # A more robust way might be to put a "None" or "Stop" sentinel message
    # for each consumer if they exit after processing.
    # For now, we'll wait for queue to be empty and then signal.
    
    print("Waiting for all messages to be processed by consumers...")
    message_queue.join() # Blocks until all items in the queue have been gotten and processed.
    print("All messages in queue have been processed.")

    # Signal consumers to stop
    for c in consumers:
        c.stop()
    
    # Wait for consumers to finish their cleanup/exit loop
    for c in consumers:
        c.join()

    print("\nSimulation complete.")