class CompressedTrie:
    def __init__(self):
        self.root = {'children': {}, 'is_end': False}

    def insert(self, word):
        node = self.root
        i = 0
        while i < len(word):
            match_found = False
            for path, child_node in list(node['children'].items()):
                if word[i] == path[0]:
                    match_len = 0
                    while match_len < len(path) and i + match_len < len(word) and word[i+match_len] == path[match_len]:
                        match_len += 1
                    
                    if match_len == len(path):
                        i += match_len
                        node = child_node
                    else:
                        new_common_path = path[:match_len]
                        new_branch_path = path[match_len:]
                        
                        new_branch_node = {'children': child_node['children'], 'is_end': child_node['is_end']}
                        child_node['children'] = {new_branch_path: new_branch_node}
                        child_node['is_end'] = False
                        child_node['children'][word[i+match_len:]] = {'children': {}, 'is_end': True}
                        
                        del node['children'][path]
                        node['children'][new_common_path] = child_node
                    match_found = True
                    break
            
            if not match_found:
                node['children'][word[i:]] = {'children': {}, 'is_end': True}
                break
            
        else:
            node['is_end'] = True

    def contains(self, word):
        node = self.root
        i = 0
        while i < len(word):
            found_path = None
            for path, child_node in node['children'].items():
                if word[i] == path[0] and word[i:i+len(path)] == path:
                    found_path = path
                    node = child_node
                    i += len(path)
                    break
            if not found_path:
                return False
        return node['is_end']

if __name__ == "__main__":
    trie = CompressedTrie()
    words = ["cat", "car", "cart", "dog", "apple"]
    for word in words:
        trie.insert(word)

    print(trie.contains("cat"))
    print(trie.contains("car"))
    print(trie.contains("cart"))
    print(trie.contains("dog"))
    print(trie.contains("apple"))
    print(trie.contains("c"))
    print(trie.contains("ca"))
    print(trie.contains("card"))