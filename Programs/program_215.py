import array
import hashlib

class BloomFilter:
    def __init__(self, size, hash_count):
        self.size = size
        self.hash_count = hash_count
        self.bit_array = array.array('B', [0] * size)

    def _hash(self, item):
        hashes = []
        for i in range(self.hash_count):
            h = hashlib.sha256(f"{item}{i}".encode()).hexdigest()
            hashes.append(int(h, 16) % self.size)
        return hashes

    def add(self, item):
        for h in self._hash(item):
            self.bit_array[h] = 1

    def check(self, item):
        for h in self._hash(item):
            if self.bit_array[h] == 0:
                return False
        return True

if __name__ == '__main__':
    bf = BloomFilter(size=100, hash_count=3)
    bf.add("apple")
    bf.add("banana")

    print(bf.check("apple"))
    print(bf.check("banana"))
    print(bf.check("cherry"))