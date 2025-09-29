import hashlib
import random

class AsymmetricCrypto:
    def __init__(self):
        self.public_key = None
        self.private_key = None
        
    def generate_keys(self):
        prime1 = random.randint(100, 200)
        prime2 = random.randint(200, 300)
        
        n = prime1 * prime2
        self.public_key = (n, prime1)
        self.private_key = (n, prime2)

def sign_message(message, private_key):
    n, p = private_key
    message_hash = hashlib.sha256(message.encode()).hexdigest()
    
    signature = ""
    for char in message_hash:
        char_code = ord(char)
        signed_code = pow(char_code, p, n)
        signature += str(signed_code)
    
    return signature

def verify_signature(message, signature, public_key):
    n, p = public_key
    message_hash = hashlib.sha256(message.encode()).hexdigest()
    
    signature_blocks = [signature[i:i+3] for i in range(0, len(signature), 3)]
    
    verified_hash = ""
    for block in signature_blocks:
        signed_code = int(block)
        verified_code = pow(signed_code, p, n)
        verified_hash += chr(verified_code)
    
    return verified_hash == message_hash

if __name__ == '__main__':
    crypto = AsymmetricCrypto()
    crypto.generate_keys()
    
    message = "This is a secret message."
    signature = sign_message(message, crypto.private_key)
    
    is_valid = verify_signature(message, signature, crypto.public_key)
    print(f"Signature is valid: {is_valid}")
    
    tampered_message = "This is a tampered message."
    is_valid_tampered = verify_signature(tampered_message, signature, crypto.public_key)
    print(f"Signature is valid for tampered message: {is_valid_tampered}")