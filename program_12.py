class TrieNode:
    def __init__(self):
        self.children = {}  # Stores mapping of character to TrieNode
        self.is_end_of_word = False # True if this node marks the end of a word

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """
        Inserts a word into the trie.
        """
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def _search_prefix(self, prefix: str) -> TrieNode:
        """
        Helper function to traverse the trie for a given prefix.
        Returns the last node of the prefix if found, otherwise None.
        """
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def search(self, word: str) -> bool:
        """
        Returns True if the word is in the trie.
        """
        node = self._search_prefix(word)
        return node is not None and node.is_end_of_word

    def starts_with(self, prefix: str) -> bool:
        """
        Returns True if there is any word in the trie that starts with the given prefix.
        """
        return self._search_prefix(prefix) is not None

# Example Usage:
trie = Trie()
trie.insert("apple")
print("Search 'apple':", trie.search("apple"))   # True
print("Search 'app':", trie.search("app"))      # False (app is a prefix, but not inserted as a full word)
print("Starts with 'app':", trie.starts_with("app")) # True
trie.insert("app")
print("Search 'app' after insert:", trie.search("app")) # True

trie.insert("banana")
print("Search 'ban':", trie.search("ban"))       # False
print("Starts with 'ban':", trie.starts_with("ban")) # True
print("Starts with 'bat':", trie.starts_with("bat")) # False