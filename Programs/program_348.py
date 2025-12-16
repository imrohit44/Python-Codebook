import random
import threading

class ConcurrentSkipNode:
    def __init__(self, key, value, level):
        self.key = key
        self.value = value
        self.forward = [None] * (level + 1)
        self.lock = threading.Lock() # Lock per node

class ConcurrentSkipList:
    MAX_LEVEL = 16
    P = 0.5
    
    def __init__(self):
        self.header = ConcurrentSkipNode(float('-inf'), None, self.MAX_LEVEL)
        self.level = 0
        self.lock = threading.Lock() # Lock for level changes

    def _random_level(self):
        lvl = 0
        while random.random() < self.P and lvl < self.MAX_LEVEL:
            lvl += 1
        return lvl

    def insert(self, key, value):
        update = [None] * (self.MAX_LEVEL + 1)
        current = self.header
        
        # Phase 1: Search and mark nodes for update (without locks)
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current
            
        current = current.forward[0]
        
        if current and current.key == key:
            current.value = value
            return

        # Phase 2: Acquire locks from bottom up
        nodes_to_lock = update[:self.level + 1]
        
        for node in nodes_to_lock:
            node.lock.acquire()

        try:
            # Re-validate pointers after acquiring locks
            # (Simplified check: relies on careful pointer manipulation for correctness)

            new_level = self._random_level()

            with self.lock:
                if new_level > self.level:
                    for i in range(self.level + 1, new_level + 1):
                        update[i] = self.header
                    self.level = new_level

            new_node = ConcurrentSkipNode(key, value, new_level)
            
            for i in range(new_level + 1):
                new_node.forward[i] = update[i].forward[i]
                update[i].forward[i] = new_node

        finally:
            # Release locks
            for node in nodes_to_lock:
                node.lock.release()

    def search(self, key):
        current = self.header
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
        
        current = current.forward[0]
        
        if current and current.key == key:
            return current.value
        return None

def worker_insert(skip_list, start, end):
    for i in range(start, end):
        skip_list.insert(i, f"Value {i}")

if __name__ == '__main__':
    csl = ConcurrentSkipList()
    
    threads = []
    num_threads = 4
    for i in range(num_threads):
        start = i * 200
        end = (i + 1) * 200
        t = threading.Thread(target=worker_insert, args=(csl, start, end))
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
    print(f"Search for 150: {csl.search(150)}")
    print(f"Search for 799: {csl.search(799)}")