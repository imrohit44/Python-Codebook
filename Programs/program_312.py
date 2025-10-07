BASE66_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

def custom_b64_encode(data):
    encoded = []
    padding = (-len(data)) % 3
    data += b'\x00' * padding
    
    for i in range(0, len(data), 3):
        chunk = data[i:i+3]
        
        b1, b2, b3 = chunk[0], chunk[1], chunk[2]
        
        idx1 = b1 >> 2
        idx2 = ((b1 & 0x03) << 4) | (b2 >> 4)
        idx3 = ((b2 & 0x0F) << 2) | (b3 >> 6)
        idx4 = b3 & 0x3F
        
        encoded.append(BASE66_CHARS[idx1])
        encoded.append(BASE66_CHARS[idx2])
        encoded.append(BASE66_CHARS[idx3])
        encoded.append(BASE66_CHARS[idx4])
        
    result = "".join(encoded)
    
    if padding == 1:
        return result[:-1] + '='
    if padding == 2:
        return result[:-2] + '=='
    return result

def custom_b64_decode(data):
    data = data.rstrip('=')
    
    byte_array = bytearray()
    
    for i in range(0, len(data), 4):
        c1, c2, c3, c4 = data[i], data[i+1], data[i+2], data[i+3]
        
        i1 = BASE66_CHARS.index(c1)
        i2 = BASE66_CHARS.index(c2)
        i3 = BASE66_CHARS.index(c3)
        i4 = BASE66_CHARS.index(c4)
        
        b1 = (i1 << 2) | (i2 >> 4)
        b2 = ((i2 & 0x0F) << 4) | (i3 >> 2)
        b3 = ((i3 & 0x03) << 6) | i4
        
        byte_array.append(b1)
        byte_array.append(b2)
        byte_array.append(b3)
        
    return bytes(byte_array[:-data.count('=') if data.count('=') else len(byte_array)])

if __name__ == '__main__':
    original_string = "Man"
    encoded = custom_b64_encode(original_string.encode('ascii'))
    decoded = custom_b64_decode(encoded)
    
    print(f"Original: {original_string}")
    print(f"Encoded: {encoded}")
    print(f"Decoded: {decoded.decode('ascii')}")