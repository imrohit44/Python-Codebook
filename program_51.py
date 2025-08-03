class Node:
    def __init__(self):
        self.children = {}
        self.suffix_link = None
        self.is_terminal = False

class SuffixTree:
    def __init__(self, text):
        self.root = Node()
        self.text = text + '$'
        self.build_tree()

    def build_tree(self):
        for i in range(len(self.text)):
            self.insert_suffix(self.text[i:])

    def insert_suffix(self, suffix):
        node = self.root
        for char in suffix:
            if char not in node.children:
                node.children[char] = Node()
            node = node.children[char]
        node.is_terminal = True

    def contains(self, substring):
        node = self.root
        for char in substring:
            if char not in node.children:
                return False
            node = node.children[char]
        return True

if __name__ == "__main__":
    text = "banana"
    st = SuffixTree(text)

    print(st.contains("ana"))
    print(st.contains("anana"))
    print(st.contains("ban"))
    print(st.contains("z"))
    print(st.contains("bana"))
    print(st.contains("nana"))