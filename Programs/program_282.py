class State:
    def __init__(self, length, link=None):
        self.length = length
        self.link = link # Suffix link
        self.next = {}   # Transition map (char -> State)

class SuffixAutomaton:
    def __init__(self):
        self.last = self.root = State(0)
        self.size = 1

    def extend(self, char):
        new_state = State(self.last.length + 1)
        self.size += 1
        
        p = self.last
        while p and char not in p.next:
            p.next[char] = new_state
            p = p.link
        
        if not p:
            new_state.link = self.root
        else:
            q = p.next[char]
            if p.length + 1 == q.length:
                new_state.link = q
            else:
                clone = State(p.length + 1, q.link)
                clone.next = q.next.copy()
                self.size += 1

                while p and p.next.get(char) == q:
                    p.next[char] = clone
                    p = p.link
                
                q.link = clone
                new_state.link = clone
        
        self.last = new_state

    def build_from_text(self, text):
        for char in text:
            self.extend(char)

    def contains(self, substring):
        node = self.root
        for char in substring:
            if char in node.next:
                node = node.next[char]
            else:
                return False
        return True

if __name__ == '__main__':
    sa = SuffixAutomaton()
    sa.build_from_text("banana")

    print(f"Contains 'ana': {sa.contains('ana')}")
    print(f"Contains 'ban': {sa.contains('ban')}")
    print(f"Contains 'nab': {sa.contains('nab')}")