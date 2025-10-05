def sieve_of_eratosthenes_bits(n):
    # Determine the required size of the integer array (32 bits per integer)
    size = (n + 31) // 32
    bit_array = [0] * size
    
    # Mark function: sets the bit for index i
    def mark(i):
        if i >= 2:
            bit_array[i // 32] |= (1 << (i % 32))
            
    # Check function: returns true if the bit for index i is set (i.e., composite)
    def is_marked(i):
        if i < 2: return True
        return (bit_array[i // 32] >> (i % 32)) & 1
    
    # Iterate through numbers starting from 2
    for i in range(2, int(n**0.5) + 1):
        if not is_marked(i):
            for multiple in range(i * i, n + 1, i):
                mark(multiple)
                
    primes = []
    for i in range(2, n + 1):
        if not is_marked(i):
            primes.append(i)
            
    return primes

if __name__ == '__main__':
    limit = 100
    primes = sieve_of_eratosthenes_bits(limit)
    print(f"Primes up to {limit}: {primes}")