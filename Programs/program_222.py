class Node:
    def __init__(self, value, color='RED'):
        self.value = value
        self.color = color
        self.parent = None
        self.left = None
        self.right = None

class RedBlackTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        if not self.root:
            self.root = Node(value, color='BLACK')
            return
            
        parent = None
        current = self.root
        while current:
            parent = current
            if value < current.value:
                current = current.left
            else:
                current = current.right
                
        new_node = Node(value, parent=parent)
        if value < parent.value:
            parent.left = new_node
        else:
            parent.right = new_node
            
    def _in_order_traversal(self, node):
        if node:
            self._in_order_traversal(node.left)
            print(node.value, node.color)
            self._in_order_traversal(node.right)
            
    def display(self):
        self._in_order_traversal(self.root)

if __name__ == '__main__':
    rb_tree = RedBlackTree()
    rb_tree.insert(50)
    rb_tree.insert(30)
    rb_tree.insert(70)
    rb_tree.insert(20)
    rb_tree.insert(40)
    
    rb_tree.display()