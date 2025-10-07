class Rope:
    def __init__(self, left=None, right=None, text=None):
        if text is not None:
            self.text = text
            self.weight = len(text)
            self.left = None
            self.right = None
        else:
            self.text = None
            self.left = left
            self.right = right
            self.weight = len(left) if left else 0

    def __len__(self):
        if self.text is not None:
            return len(self.text)
        return self.weight + (len(self.right) if self.right else 0)

    def concatenate(self, other):
        if not self.text and not self.left and not self.right:
            return other
        if not other.text and not other.left and not other.right:
            return self
            
        return Rope(left=self, right=other)

    def __repr__(self):
        return f"Rope(Weight={self.weight}, Length={len(self)})"

    def to_string(self):
        if self.text is not None:
            return self.text
        
        left_str = self.left.to_string() if self.left else ""
        right_str = self.right.to_string() if self.right else ""
        return left_str + right_str

if __name__ == '__main__':
    r1 = Rope(text="Hello, ")
    r2 = Rope(text="World!")
    
    r3 = r1.concatenate(r2)
    print(f"Rope length: {len(r3)}")
    print(f"Rope structure: {r3}")
    print(f"Concatenated String: {r3.to_string()}")