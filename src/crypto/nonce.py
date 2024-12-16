import hashlib
import secrets
import struct

class Nonce:
    def __init__(self, keys=None, nonce=None):
        if keys is None and nonce is None:
            self.nonce = bytes(secrets.token_bytes(24))
            return
        
        if keys:
            b2b = hashlib.blake2b(digest_size=24)
            
            if nonce:
                b2b.update(nonce)
            
            for key in keys:
                b2b.update(key)
            
            self.nonce = b2b.digest()
        elif nonce:
            self.nonce = nonce
    
    def bytes(self):
        return self.nonce
    
    def increment(self):
        temp = bytearray(self.nonce)
        value = struct.unpack_from("<I", temp, 0)[0]
        
        value += 2
        struct.pack_into("<I", temp, 0, value)
        
        self.nonce = bytes(temp)