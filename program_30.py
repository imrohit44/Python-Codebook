from collections import OrderedDict, defaultdict
import heapq
import time

# --- LRU Cache Implementation (Problem 1 revisited, slightly adjusted) ---
class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        # OrderedDict maintains insertion order (or order of last access if moved_to_end is True)
        self.cache = OrderedDict()
        self.hits = 0
        self.misses = 0

    def get(self, key: any) -> any:
        if key in self.cache:
            self.hits += 1
            value = self.cache.pop(key) # Remove and re-insert to mark as recently used
            self.cache[key] = value
            return value
        self.misses += 1
        return -1 # Not found

    def put(self, key: any, value: any) -> None:
        if key in self.cache:
            self.cache.pop(key) # Remove existing to update position
        elif len(self.cache) >= self.capacity:
            # Evict LRU item (first item in OrderedDict)
            lru_key = next(iter(self.cache))
            del self.cache[lru_key]
            # print(f"  LRU Eviction: Evicted {lru_key} from L1 Cache.")
        self.cache[key] = value

    def __len__(self):
        return len(self.cache)

    def __str__(self):
        return f"LRUCache(Capacity={self.capacity}, Current={len(self.cache)}, Hits={self.hits}, Misses={self.misses}, Content={list(self.cache.keys())})"

# --- LFU Cache Implementation ---
class LFUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # key: value
        self.frequencies = defaultdict(int) # key: frequency_count
        # Use a min-heap to store (frequency, timestamp, key) for eviction
        # Timestamp is used as a tie-breaker for elements with same frequency (LRU-like for ties)
        self.min_heap = [] # Stores (frequency, insertion_time, key)
        self.current_time = 0 # To provide unique timestamps for tie-breaking
        self.hits = 0
        self.misses = 0

    def _update_frequency(self, key):
        old_freq = self.frequencies[key]
        self.frequencies[key] += 1
        new_freq = self.frequencies[key]
        # Rebuild heap or update specifically if needed. For simplicity, we just
        # increment frequency. The old entry in heap remains but is ignored if key isn't in cache.
        # A more robust LFU would update heap entries directly, which is complex for Python's heapq.
        # For this problem, we'll let "stale" entries accumulate in the heap,
        # and only process valid keys when popping.
        
        # When an item's frequency changes, its position in the heap needs to be updated.
        # Since heapq doesn't support arbitrary updates, a common strategy is to:
        # 1. Mark the old entry as invalid (e.g., store key with unique ID for old entry).
        # 2. Add a new entry to the heap with the updated frequency.
        # 3. When popping, skip invalid entries.
        self.current_time += 1
        heapq.heappush(self.min_heap, (new_freq, self.current_time, key))

    def get(self, key: any) -> any:
        if key in self.cache:
            self.hits += 1
            self._update_frequency(key) # Increment frequency on access
            return self.cache[key]
        self.misses += 1
        return -1 # Not found

    def put(self, key: any, value: any) -> None:
        if self.capacity == 0: return # Handle zero capacity

        if key in self.cache:
            self.cache[key] = value
            self._update_frequency(key)
        else:
            if len(self.cache) >= self.capacity:
                # Evict LFU item
                while self.min_heap:
                    freq, _, lfu_key = heapq.heappop(self.min_heap)
                    # Check if the key is still in cache and its frequency matches
                    if lfu_key in self.cache and self.frequencies[lfu_key] == freq:
                        del self.cache[lfu_key]
                        del self.frequencies[lfu_key]
                        # print(f"  LFU Eviction: Evicted {lfu_key} from L2 Cache.")
                        break
                    # If not, it's a stale entry, keep popping
                else:
                    # Should not happen if logic is correct and capacity > 0
                    print("  LFU Warning: Heap empty but cache is full. This indicates an issue.")

            self.cache[key] = value
            self.frequencies[key] = 1 # New item, frequency 1
            self.current_time += 1
            heapq.heappush(self.min_heap, (1, self.current_time, key)) # Add to heap

    def __len__(self):
        return len(self.cache)
    
    def __str__(self):
        return f"LFUCache(Capacity={self.capacity}, Current={len(self.cache)}, Hits={self.hits}, Misses={self.misses}, Content={list(self.cache.keys())})"

# --- Simulated Data Source ---
class DataSource:
    def __init__(self):
        self._data = {
            "itemA": "Value for A",
            "itemB": "Value for B",
            "itemC": "Value for C",
            "itemD": "Value for D",
            "itemE": "Value for E",
            "itemF": "Value for F",
            "itemG": "Value for G",
            "itemH": "Value for H",
            "itemI": "Value for I",
            "itemJ": "Value for J",
        }
        self.fetch_count = 0

    def fetch(self, key: any) -> any:
        self.fetch_count += 1
        # Simulate network/disk latency
        time.sleep(0.01) 
        print(f"  DataSource: Fetching '{key}'...")
        return self._data.get(key, f"Value not found for {key}")

# --- Multi-Level Cache Orchestrator ---
class MultiLevelCache:
    def __init__(self, l1_capacity: int, l2_capacity: int):
        self.l1_cache = LRUCache(l1_capacity)
        self.l2_cache = LFUCache(l2_capacity)
        self.data_source = DataSource()
        self.total_hits = 0
        self.total_misses = 0

    def get(self, key: any) -> any:
        print(f"\nRequesting: {key}")
        
        # 1. Check L1 Cache
        value = self.l1_cache.get(key)
        if value != -1:
            print(f"  L1 Hit for '{key}'. Value: '{value}'")
            self.total_hits += 1
            return value

        # 2. Check L2 Cache (L1 Miss)
        value = self.l2_cache.get(key)
        if value != -1:
            print(f"  L2 Hit for '{key}'. Value: '{value}' (L1 Miss)")
            self.l1_cache.put(key, value) # Add to L1 as it's recently used
            self.total_hits += 1
            return value

        # 3. Fetch from Data Source (L1 & L2 Miss)
        print(f"  Cache Miss for '{key}'. Fetching from Data Source...")
        self.total_misses += 1
        value = self.data_source.fetch(key)
        
        # Add to both L1 and L2
        self.l1_cache.put(key, value)
        self.l2_cache.put(key, value)
        return value

    def get_stats(self):
        return {
            "total_hits": self.total_hits,
            "total_misses": self.total_misses,
            "l1_stats": str(self.l1_cache),
            "l2_stats": str(self.l2_cache),
            "data_source_fetches": self.data_source.fetch_count
        }

# Example Usage:
if __name__ == "__main__":
    cache_system = MultiLevelCache(l1_capacity=2, l2_capacity=3)

    print("--- Initial State ---")
    print("L1:", cache_system.l1_cache)
    print("L2:", cache_system.l2_cache)

    # Sequence of requests
    cache_system.get("itemA") # Miss (L1, L2), Fetch. L1: A, L2: A
    cache_system.get("itemB") # Miss (L1, L2), Fetch. L1: B,A L2: B,A
    cache_system.get("itemC") # Miss (L1, L2), Fetch. L1: C,B (A evicted), L2: C,B,A
    # L1: C(new), B(LRU), L2: C(freq1), B(freq1), A(freq1)

    print("\n--- After first set of requests ---")
    print("L1:", cache_system.l1_cache)
    print("L2:", cache_system.l2_cache)
    print(cache_system.get_stats())

    cache_system.get("itemB") # L1 Hit. L1: B,C (B moved to front). L2: B freq (2)
    cache_system.get("itemD") # Miss (L1, L2), Fetch. L1: D,B (C evicted). L2: D(new,1), A(1), B(2) (C evicted if L2 full)
    # L2 has capacity 3. If C was freq 1, A was freq 1, B was freq 2. A or C would be evicted.
    # The LFU min_heap will pop (1, timestamp, key) for A or C.

    print("\n--- After second set of requests ---")
    print("L1:", cache_system.l1_cache)
    print("L2:", cache_system.l2_cache)
    print(cache_system.get_stats())

    cache_system.get("itemB") # L1 Hit. L1: B,D. L2: B freq (3)
    cache_system.get("itemA") # L2 Hit. L1: A,B (D evicted). L2: A freq (2)
    cache_system.get("itemE") # Miss (L1, L2), Fetch. L1: E,A (B evicted). L2: E(new,1), D/C?

    print("\n--- After third set of requests ---")
    print("L1:", cache_system.l1_cache)
    print("L2:", cache_system.l2_cache)
    print(cache_system.get_stats())