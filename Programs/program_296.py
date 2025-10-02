class CartesianProduct:
    def __init__(self, *iterables):
        self.pools = [tuple(iterable) for iterable in iterables]
        self.dimensions = [len(pool) for pool in self.pools]
        self.indices = [0] * len(self.pools)
        self.is_finished = False

    def __iter__(self):
        return self

    def __next__(self):
        if self.is_finished:
            raise StopIteration
            
        result = tuple(pool[i] for pool, i in zip(self.pools, self.indices))
        
        # Advance indices
        for i in range(len(self.indices) - 1, -1, -1):
            self.indices[i] += 1
            if self.indices[i] < self.dimensions[i]:
                break
            
            self.indices[i] = 0
            if i == 0:
                self.is_finished = True
                
        return result

if __name__ == '__main__':
    colors = ['Red', 'Green']
    sizes = [1, 2, 3]
    materials = ['Cotton', 'Wool']
    
    product = CartesianProduct(colors, sizes, materials)
    
    for item in product:
        print(item)