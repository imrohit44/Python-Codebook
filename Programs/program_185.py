class FenwickTree:
    def __init__(self, size):
        self.tree = [0] * (size + 1)
        self.size = size

    def update(self, index, value):
        index += 1
        while index <= self.size:
            self.tree[index] += value
            index += index & (-index)

    def query(self, index):
        index += 1
        total = 0
        while index > 0:
            total += self.tree[index]
            index -= index & (-index)
        return total
    
    def get_range_sum(self, start, end):
        return self.query(end) - self.query(start - 1)

if __name__ == '__main__':
    arr = [1, 2, 3, 4, 5]
    ft = FenwickTree(len(arr))
    for i, val in enumerate(arr):
        ft.update(i, val)
    
    print(f"Prefix sum up to index 2: {ft.query(2)}")
    print(f"Range sum from index 1 to 3: {ft.get_range_sum(1, 3)}")