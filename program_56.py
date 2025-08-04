class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

def post_order_traversal(root):
    if not root:
        return []
    
    result = []
    stack1 = [root]
    stack2 = []
    
    while stack1:
        node = stack1.pop()
        stack2.append(node)
        if node.left:
            stack1.append(node.left)
        if node.right:
            stack1.append(node.right)
            
    while stack2:
        result.append(stack2.pop().value)
        
    return result

if __name__ == "__main__":
    root = Node(1, Node(2, Node(4), Node(5)), Node(3, Node(6), Node(7)))
    print(post_order_traversal(root))