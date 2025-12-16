def rabin_karp(text, pattern, d=256, q=101):
    N = len(text)
    M = len(pattern)
    
    if M > N:
        return -1 # Pattern is longer than text

    p_hash = 0  # hash value for pattern
    t_hash = 0  # hash value for text window
    h = 1       # d^(M-1) % q

    # Precompute d^(M-1) % q
    for i in range(M - 1):
        h = (h * d) % q

    # Calculate initial hash for pattern and first text window
    for i in range(M):
        p_hash = (d * p_hash + ord(pattern[i])) % q
        t_hash = (d * t_hash + ord(text[i])) % q

    # Slide the pattern over the text
    for i in range(N - M + 1):
        if p_hash == t_hash:
            # Check for spurious hit (full match check)
            if text[i:i+M] == pattern:
                return i
        
        # Calculate rolling hash for next window (if not the last iteration)
        if i < N - M:
            # Subtract old character, multiply by d, add new character
            t_hash = (d * (t_hash - ord(text[i]) * h) + ord(text[i + M])) % q
            
            # Ensure t_hash is non-negative
            if t_hash < 0:
                t_hash += q
                
    return -1

if __name__ == '__main__':
    text = "GEEKSFORGEEKS"
    pattern = "FOR"
    
    index = rabin_karp(text, pattern)
    print(f"Pattern '{pattern}' found at index: {index}")