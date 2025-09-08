import array
import math
import mmh3 # pip install mmh3

class OptimalBloomFilter:
    def __init__(self, expected_elements: int, false_positive_rate: float):
        """
        Initializes the Bloom Filter by calculating optimal size and hash functions.

        Args:
            expected_elements (int): The approximate number of items expected to be added.
            false_positive_rate (float): The desired false positive rate (e.g., 0.01 for 1%).
                                         Must be between 0 and 1 (exclusive).
        """
        if not (0 < false_positive_rate < 1):
            raise ValueError("False positive rate must be between 0 and 1 (exclusive).")
        if expected_elements <= 0:
            raise ValueError("Expected elements must be a positive integer.")

        self.expected_elements = expected_elements
        self.false_positive_rate = false_positive_rate

        # Calculate optimal 'm' (size of bit array)
        # m = -(n * ln(p)) / (ln(2)^2)
        m = - (expected_elements * math.log(false_positive_rate)) / (math.log(2) ** 2)
        self.size = int(m)
        if self.size < 1: # Ensure size is at least 1
            self.size = 1 

        # Calculate optimal 'k' (number of hash functions)
        # k = (m/n) * ln(2)
        k = (self.size / expected_elements) * math.log(2)
        self.num_hash_functions = int(k)
        if self.num_hash_functions < 1: # Ensure at least one hash function
            self.num_hash_functions = 1

        self.bit_array = array.array('B', [0] * self.size)
        self.current_elements = 0

        print(f"Optimal Bloom Filter calculated parameters:")
        print(f"  Expected Elements (n): {expected_elements}")
        print(f"  Desired False Positive Rate (p): {false_positive_rate}")
        print(f"  Calculated Bit Array Size (m): {self.size}")
        print(f"  Calculated Number of Hash Functions (k): {self.num_hash_functions}")
        print("-" * 50)

    def _get_hash_indices(self, item) -> list[int]:
        """
        Generates `num_hash_functions` hash indices for an item using mmh3.
        """
        indices = []
        item_bytes = str(item).encode('utf-8')
        for i in range(self.num_hash_functions):
            h = mmh3.hash(item_bytes, i) # Use i as seed for different hashes
            index = h % self.size
            indices.append(index)
        return indices

    def add(self, item) -> None:
        """
        Adds an item to the Bloom Filter.
        """
        for index in self._get_hash_indices(item):
            self.bit_array[index] = 1
        self.current_elements += 1
        # print(f"Added: '{item}'")

    def contains(self, item) -> bool:
        """
        Checks if an item might be in the Bloom Filter.
        Returns True for possible presence (may be a false positive), False for definite absence.
        """
        for index in self._get_hash_indices(item):
            if self.bit_array[index] == 0:
                # print(f"'{item}': Definitely NOT in the set (bit at index {index} is 0).")
                return False
        # print(f"'{item}': Possibly in the set (all relevant bits are 1).")
        return True
    
    def get_effective_false_positive_rate(self) -> float:
        """
        Calculates the theoretical false positive rate based on current elements,
        size (m), and hash functions (k).
        p = (1 - exp(-k * n / m))^k
        """
        if self.size == 0 or self.current_elements == 0:
            return 0.0 # No elements, no false positives
        
        # Calculate the probability of a single bit being 0 after n insertions
        # This is (1 - 1/m)^(k*n)
        # The probability of a bit being 1 after k insertions is 1 - (1 - 1/m)^k
        # So, the probability of *all k* bits for a *new* element being 1 is (1 - (1 - 1/m)^k)^k
        # More accurately, p = (1 - e^(-kn/m))^k
        
        prob_bit_is_zero = math.exp(-self.num_hash_functions * self.current_elements / self.size)
        effective_fpr = (1 - prob_bit_is_zero) ** self.num_hash_functions
        return effective_fpr


# Example Usage:
if __name__ == "__main__":
    # Test 1: Low expected elements, low false positive rate
    bf1 = OptimalBloomFilter(expected_elements=100, false_positive_rate=0.01)

    words_to_add = [f"word_{i}" for i in range(100)]
    for word in words_to_add:
        bf1.add(word)

    print("\n--- Checking for existing words (BF1) ---")
    print(f"'word_50' exists: {bf1.contains('word_50')}")
    print(f"'word_99' exists: {bf1.contains('word_99')}")

    print("\n--- Checking for non-existing words (BF1) ---")
    non_existing_words = [f"not_word_{i}" for i in range(50)]
    false_positives = 0
    for word in non_existing_words:
        if bf1.contains(word):
            false_positives += 1
            print(f"  False positive: '{word}'")
    print(f"Total false positives for BF1: {false_positives}/{len(non_existing_words)}")
    print(f"Effective False Positive Rate for BF1: {bf1.get_effective_false_positive_rate():.6f}")


    # Test 2: Higher expected elements, slightly higher false positive rate
    bf2 = OptimalBloomFilter(expected_elements=1000, false_positive_rate=0.005)

    words_to_add_2 = [f"unique_id_{i}" for i in range(1000)]
    for word in words_to_add_2:
        bf2.add(word)

    print("\n--- Checking for existing words (BF2) ---")
    print(f"'unique_id_500' exists: {bf2.contains('unique_id_500')}")

    print("\n--- Checking for non-existing words (BF2) ---")
    non_existing_words_2 = [f"new_id_{i}" for i in range(500)]
    false_positives_2 = 0
    for word in non_existing_words_2:
        if bf2.contains(word):
            false_positives_2 += 1
    print(f"Total false positives for BF2: {false_positives_2}/{len(non_existing_words_2)}")
    print(f"Effective False Positive Rate for BF2: {bf2.get_effective_false_positive_rate():.6f}")