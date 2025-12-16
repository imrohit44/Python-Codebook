from collections import OrderedDict

class LRUPaging:
    def __init__(self, capacity):
        self.capacity = capacity
        self.page_frames = OrderedDict()  # Key: page number, Value: 1 (placeholder)
        self.page_faults = 0

    def reference_page(self, page_number):
        if page_number in self.page_frames:
            # Hit: Move to the end (Most Recently Used)
            self.page_frames.move_to_end(page_number)
            return False # No fault
        else:
            # Fault: Page not in memory
            self.page_faults += 1
            
            if len(self.page_frames) >= self.capacity:
                # Evict LRU (first item)
                lru_page = next(iter(self.page_frames))
                del self.page_frames[lru_page]
                # print(f"Fault: Evicting {lru_page}")

            # Add new page
            self.page_frames[page_number] = 1
            return True # Fault occurred

    def get_fault_count(self):
        return self.page_faults

if __name__ == '__main__':
    # Page reference string
    references = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]
    
    lru = LRUPaging(capacity=3)
    
    for page in references:
        lru.reference_page(page)

    print(f"Page Faults (Capacity 3): {lru.get_fault_count()}")