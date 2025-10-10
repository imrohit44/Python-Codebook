def manacher(text):
    T = '#'.join('^{}$'.format(text))
    n = len(T)
    P = [0] * n
    C = R = 0
    
    for i in range(1, n - 1):
        i_mirror = 2 * C - i
        
        if R > i:
            P[i] = min(R - i, P[i_mirror])
        
        while T[i + 1 + P[i]] == T[i - 1 - P[i]]:
            P[i] += 1
            
        if i + P[i] > R:
            C = i
            R = i + P[i]
            
    max_len = 0
    center_index = 0
    for i in range(1, n - 1):
        if P[i] > max_len:
            max_len = P[i]
            center_index = i
            
    start_index = (center_index - max_len) // 2
    return text[start_index: start_index + max_len]

if __name__ == '__main__':
    s1 = "babad"
    print(f"LPS of '{s1}': {manacher(s1)}")
    
    s2 = "cbbd"
    print(f"LPS of '{s2}': {manacher(s2)}")
    
    s3 = "abacaba"
    print(f"LPS of '{s3}': {manacher(s3)}")