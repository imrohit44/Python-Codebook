import hashlib
import bisect
import time
from collections import OrderedDict

class ConsistentHasher:
    def __init__(self, replicas=100):
        self.replicas = replicas
        self.ring = OrderedDict()
        self.sorted_keys = []
        self.nodes = set()

    def add_node(self, node):
        if node in self.nodes:
            return
        self.nodes.add(node)
        for i in range(self.replicas):
            key = self._hash(f"{node}:{i}")
            self.ring[key] = node
        self.sorted_keys = sorted(self.ring.keys())

    def remove_node(self, node):
        if node not in self.nodes:
            return
        self.nodes.remove(node)
        for i in range(self.replicas):
            key = self._hash(f"{node}:{i}")
            del self.ring[key]
        self.sorted_keys = sorted(self.ring.keys())

    def get_node(self, key):
        if not self.ring:
            return None
        hash_key = self._hash(key)
        idx = bisect.bisect_left(self.sorted_keys, hash_key)
        if idx == len(self.sorted_keys):
            idx = 0
        return self.ring[self.sorted_keys[idx]]

    def _hash(self, key):
        return int(hashlib.md5(key.encode()).hexdigest(), 16)

class CacheNode:
    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity
        self.cache = OrderedDict()

    def set(self, key, value):
        if key in self.cache:
            self.cache.pop(key)
        elif len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)
        self.cache[key] = value

    def get(self, key):
        if key in self.cache:
            value = self.cache.pop(key)
            self.cache[key] = value
            return value
        return None

class DistributedCacheClient:
    def __init__(self, nodes, capacity):
        self.nodes = {node: CacheNode(node, capacity) for node in nodes}
        self.hasher = ConsistentHasher()
        for node in nodes:
            self.hasher.add_node(node)

    def set(self, key, value):
        node_name = self.hasher.get_node(key)
        if node_name:
            self.nodes[node_name].set(key, value)
        
    def get(self, key):
        node_name = self.hasher.get_node(key)
        if node_name:
            return self.nodes[node_name].get(key)
        return None

if __name__ == "__main__":
    nodes = ["node1", "node2", "node3"]
    client = DistributedCacheClient(nodes, capacity=2)
    
    for i in range(10):
        key = f"key_{i}"
        value = f"value_{i}"
        client.set(key, value)
    
    print("Initial cache state:")
    for name, node in client.nodes.items():
        print(f"Node {name}: {list(node.cache.keys())}")
    
    print("\nGetting values:")
    print(f"Getting key_5: {client.get('key_5')}")
    print(f"Getting key_8: {client.get('key_8')}")
    
    print("\nAdding a new node:")
    client.hasher.add_node("node4")
    client.nodes["node4"] = CacheNode("node4", 2)
    client.set("key_10", "value_10")
    
    for name, node in client.nodes.items():
        print(f"Node {name}: {list(node.cache.keys())}")
    
    print("\nRemoving node2:")
    del client.nodes["node2"]
    client.hasher.remove_node("node2")
    
    for name, node in client.nodes.items():
        print(f"Node {name}: {list(node.cache.keys())}")