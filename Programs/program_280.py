class PList:
    def __init__(self, head=None, tail=None):
        self._head = head
        self._tail = tail # Reference to the rest of the list (another PList or None)
        self._length = 0
        
        if tail is not None:
            self._length = tail._length + 1
        elif head is not None:
            self._length = 1

    def prepend(self, value):
        return PList(head=value, tail=self)

    def __len__(self):
        return self._length

    def __iter__(self):
        current = self
        while current._head is not None:
            yield current._head
            current = current._tail
    
    def __repr__(self):
        return "PList(" + ", ".join(map(str, self)) + ")"

    def __getitem__(self, index):
        if index < 0 or index >= self._length:
            raise IndexError("PList index out of range")
        
        current = self
        for i in range(self._length - 1 - index):
            current = current._tail
        
        return current._head

if __name__ == '__main__':
    p1 = PList().prepend(3).prepend(2).prepend(1)
    print(f"P1: {p1}, Length: {len(p1)}")
    
    p2 = p1.prepend(0)
    print(f"P2: {p2}, Length: {len(p2)}")
    
    print(f"P1 after P2 creation (unmodified): {p1}")
    print(f"P2[0]: {p2[0]}, P2[3]: {p2[3]}")