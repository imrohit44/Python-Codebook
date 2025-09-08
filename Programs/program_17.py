import array
import mmh3 # A fast non-cryptographic hash function, install with `pip install mmh3`

class BloomFilter:
    def __init__(self, size: int, num_hash_functions: int):
        """
        Initializes the Bloom Filter.

        Args:
            size (int): The size of the bit array (number of bits).
            num_hash_functions (int): The number of hash functions to use.
        """
        if size <= 0 or num_hash_functions <= 0:
            raise ValueError("Size and number of hash functions must be positive integers.")

        self.size = size
        self.num_hash_functions = num_hash_functions
        # Use an array of unsigned chars for memory efficiency (8 bits per byte)
        # Python's list of booleans would be less memory efficient.
        # This acts as our bit array where each element is effectively 0 or 1.
        self.bit_array = array.array('B', [0] * size) 

        print(f"Bloom Filter initialized: Size={self.size}, Hash Functions={self.num_hash_functions}")

    def _get_hash_indices(self, item) -> list[int]:
        """
        Generates `num_hash_functions` hash indices for an item.
        Uses mmh3 for better distribution and combines with a simple offset.
        """
        indices = []
        # Encode the item to bytes for hashing
        item_bytes = str(item).encode('utf-8') 
        for i in range(self.num_hash_functions):
            # mmh3.hash accepts a seed for different hash values
            # Using i as a seed for different hash functions
            h = mmh3.hash(item_bytes, i) 
            index = h % self.size
            indices.append(index)
        return indices

    def add(self, item) -> None:
        """
        Adds an item to the Bloom Filter.
        """
        for index in self._get_hash_indices(item):
            self.bit_array[index] = 1
        print(f"Added: '{item}'")

    def contains(self, item) -> bool:
        """
        Checks if an item might be in the Bloom Filter.
        Returns True for possible presence (may be a false positive), False for definite absence.
        """
        for index in self._get_hash_indices(item):
            if self.bit_array[index] == 0:
                print(f"'{item}': Definitely NOT in the set (bit at index {index} is 0).")
                return False
        print(f"'{item}': Possibly in the set (all relevant bits are 1).")
        return True

# Example Usage:
if __name__ == "__main__":
    # A larger size and more hash functions reduce false positive rate
    bf = BloomFilter(size=100, num_hash_functions=5)

    words_to_add = ["apple", "banana", "cherry", "date", "elderberry"]
    for word in words_to_add:
        bf.add(word)

    print("\n--- Checking for existing words ---")
    print(bf.contains("apple"))      # Should be True
    print(bf.contains("banana"))     # Should be True
    print(bf.contains("elderberry")) # Should be True

    print("\n--- Checking for non-existing words (expecting False or a false positive) ---")
    print(bf.contains("grape"))      # Should be False
    print(bf.contains("kiwi"))       # Should be False
    print(bf.contains("orange"))     # Should be False (or a false positive)
    print(bf.contains("averyuncommonwordthatisnotpresent")) # Should be False

    print("\n--- Testing a potential false positive (rare but possible) ---")
    # To demonstrate a false positive, you'd need to carefully craft inputs or
    # run many tests with a small filter. Let's try one more random word.
    print(bf.contains("watermelon")) # Likely False, but could be a false positive if lucky/unlucky

    # Test with a smaller filter to increase chance of false positive
    print("\n--- Testing with a smaller filter (higher chance of false positives) ---")
    bf_small = BloomFilter(size=20, num_hash_functions=3)
    bf_small.add("cat")
    bf_small.add("dog")
    print(bf_small.contains("cat"))
    print(bf_small.contains("dog"))
    print(bf_small.contains("bird")) # Might be a false positive here more often
    print(bf_small.contains("rat"))