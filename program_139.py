def build_suffix_array(text):
    n = len(text)
    suffixes = [(text[i:], i) for i in range(n)]
    suffixes.sort(key=lambda item: item[0])
    suffix_array = [suffix[1] for suffix in suffixes]
    return suffix_array

def search_suffix_array(text, suffix_array, pattern):
    n = len(text)
    m = len(pattern)
    low, high = 0, n - 1
    
    while low <= high:
        mid = (low + high) // 2
        suffix = text[suffix_array[mid]:]
        
        if pattern == suffix[:m]:
            return suffix_array[mid]
        elif pattern < suffix[:m]:
            high = mid - 1
        else:
            low = mid + 1
            
    return -1

if __name__ == '__main__':
    text = "banana"
    sa = build_suffix_array(text)
    print(f"Suffix array for '{text}': {sa}")

    print(f"Found 'ana' at index: {search_suffix_array(text, sa, 'ana')}")
    print(f"Found 'ban' at index: {search_suffix_array(text, sa, 'ban')}")  