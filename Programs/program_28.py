class DisjointSetUnion:
    def __init__(self, elements):
        """
        Initializes the DSU structure.
        Each element is initially in its own set.
        Args:
            elements (iterable): An iterable of initial elements.
        """
        self.parent = {element: element for element in elements}
        self.rank = {element: 0 for element in elements} # For Union by Rank optimization
        # self.size = {element: 1 for element in elements} # Alternative for Union by Size

    def add_element(self, element):
        """Adds a new element, creating a new singleton set for it."""
        if element not in self.parent:
            self.parent[element] = element
            self.rank[element] = 0
            # self.size[element] = 1

    def find(self, element):
        """
        Finds the representative (root) of the set containing 'element'.
        Implements Path Compression.
        """
        if element not in self.parent:
            raise ValueError(f"Element '{element}' not found in any set.")

        # If element is not its own parent, it's not the root
        if self.parent[element] != element:
            # Recursively find the root and compress the path
            self.parent[element] = self.find(self.parent[element])
        return self.parent[element]

    def union(self, element1, element2):
        """
        Merges the sets containing 'element1' and 'element2'.
        Implements Union by Rank.
        Returns True if a union occurred, False if they were already in the same set.
        """
        root1 = self.find(element1)
        root2 = self.find(element2)

        if root1 != root2:
            # Union by Rank: attach the smaller rank tree under the root of the larger rank tree
            if self.rank[root1] < self.rank[root2]:
                self.parent[root1] = root2
            elif self.rank[root2] < self.rank[root1]:
                self.parent[root2] = root1
            else:
                # If ranks are equal, pick one as root and increment its rank
                self.parent[root2] = root1
                self.rank[root1] += 1
            
            # Alternative: Union by Size
            # if self.size[root1] < self.size[root2]:
            #     self.parent[root1] = root2
            #     self.size[root2] += self.size[root1]
            # else:
            #     self.parent[root2] = root1
            #     self.size[root1] += self.size[root2]

            return True # A union occurred
        return False # Already in the same set

    def get_sets(self):
        """Returns a dictionary where keys are set representatives and values are lists of elements in that set."""
        sets = {}
        for element in self.parent:
            root = self.find(element)
            if root not in sets:
                sets[root] = []
            sets[root].append(element)
        return sets

# Example Usage:
if __name__ == "__main__":
    elements = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    dsu = DisjointSetUnion(elements)

    print("Initial sets:", dsu.get_sets())

    dsu.union('A', 'B')
    print("\nUnion A, B:", ddsu.get_sets()) # A-B

    dsu.union('B', 'C')
    print("Union B, C:", dsu.get_sets()) # A-B-C

    dsu.union('D', 'E')
    print("Union D, E:", dsu.get_sets()) # D-E

    dsu.union('F', 'G')
    print("Union F, G:", dsu.get_sets()) # F-G

    print("\nFind A:", dsu.find('A'))
    print("Find B:", dsu.find('B'))
    print("Are A and C connected?", dsu.find('A') == dsu.find('C')) # Should be True

    dsu.union('C', 'F')
    print("\nUnion C, F:", dsu.get_sets()) # A-B-C-F-G

    print("Are D and F connected?", dsu.find('D') == dsu.find('F')) # Should be False

    dsu.union('E', 'A')
    print("\nUnion E, A:", dsu.get_sets()) # All connected

    print("Are D and F connected now?", dsu.find('D') == dsu.find('F')) # Should be True

    # Add a new element
    dsu.add_element('H')
    print("\nAdded H:", dsu.get_sets())
    dsu.union('H', 'A')
    print("Union H, A:", dsu.get_sets())