class DSU:
    def __init__(self, n):
        self.parent = list(range(n))

    def find(self, i):
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j):
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i != root_j:
            self.parent[root_i] = root_j
            return True
        return False

def kruskal_mst(vertices, edges):
    edges.sort(key=lambda x: x[2])
    dsu = DSU(len(vertices))
    mst = []
    mst_weight = 0
    
    for u, v, weight in edges:
        u_idx = vertices.index(u)
        v_idx = vertices.index(v)
        
        if dsu.union(u_idx, v_idx):
            mst.append((u, v, weight))
            mst_weight += weight
            
    return mst, mst_weight

if __name__ == '__main__':
    vertices = ['A', 'B', 'C', 'D', 'E']
    edges = [
        ('A', 'B', 1), ('A', 'C', 4),
        ('B', 'C', 6), ('B', 'D', 4),
        ('C', 'D', 3), ('C', 'E', 2),
        ('D', 'E', 3)
    ]
    
    mst, weight = kruskal_mst(vertices, edges)
    print(f"MST Edges: {mst}")
    print(f"Total Weight: {weight}")