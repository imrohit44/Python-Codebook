class HashTable:
    def __init__(self, size=16):
        self.size = size
        self.keys = [None] * size
        self.values = [None] * size
        self.count = 0

    def _hash(self, key):
        return hash(key) % self.size

    def _probe(self, index, i):
        return (index + i * i) % self.size

    def put(self, key, value):
        h = self._hash(key)
        for i in range(self.size):
            new_h = self._probe(h, i)
            if self.keys[new_h] is None or self.keys[new_h] == key:
                if self.keys[new_h] is None:
                    self.count += 1
                self.keys[new_h] = key
                self.values[new_h] = value
                return
        raise OverflowError("Hash table is full")

    def get(self, key):
        h = self._hash(key)
        for i in range(self.size):
            new_h = self._probe(h, i)
            if self.keys[new_h] == key:
                return self.values[new_h]
            if self.keys[new_h] is None:
                return None
        return None

if __name__ == '__main__':
    ht = HashTable(size=7)
    ht.put('A', 10)
    ht.put('B', 20)
    ht.put('C', 30)
    
    ht.put('I', 90) # Collision with 'B' (hash 2)
    
    print(f"Key A: {ht.get('A')}")
    print(f"Key B: {ht.get('B')}")
    print(f"Key I: {ht.get('I')}")
    print(f"Key Z: {ht.get('Z')}")