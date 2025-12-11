import random

class TreapNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.priority = random.randint(0, 100)
        self.left = None
        self.right = None

class Treap:
    def __init__(self):
        self.root = None

    def _rotate_left(self, x):
        y = x.right
        x.right = y.left
        y.left = x
        return y

    def _rotate_right(self, y):
        x = y.left
        y.left = x.right
        x.right = y
        return x

    def insert(self, root, key, value):
        if root is None:
            return TreapNode(key, value)
        
        if key < root.key:
            root.left = self.insert(root.left, key, value)
            if root.left and root.left.priority > root.priority:
                root = self._rotate_right(root)
        elif key > root.key:
            root.right = self.insert(root.right, key, value)
            if root.right and root.right.priority > root.priority:
                root = self._rotate_left(root)
        else:
            root.value = value
            
        return root

    def add(self, key, value):
        self.root = self.insert(self.root, key, value)

    def _inorder_traversal(self, node):
        if node:
            self._inorder_traversal(node.left)
            print(f"Key: {node.key}, Priority: {node.priority}")
            self._inorder_traversal(node.right)
            
    def display_inorder(self):
        self._inorder_traversal(self.root)

if __name__ == '__main__':
    treap = Treap()
    keys = [50, 30, 70, 20, 40, 60, 80]
    random.shuffle(keys)
    
    for k in keys:
        treap.add(k, f"Value {k}")
    
    treap.display_inorder()