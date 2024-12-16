import secrets
from _tweetnacl import (crypto_box_afternm,crypto_box_beforenm,crypto_scalarmult_base,crypto_box_open_afternm)

from .nonce import Nonce

class PepperCrypto:
    def __init__(self):
        # TODO: move public key into a config
        self.server_public_key = bytes.fromhex("F7C80C59E42D4165A32D5D440A6939D54D18BB7F1B2335E85650673C27AA974F")
        self.client_secret_key = bytes(secrets.token_bytes(32))
        self.client_public_key = crypto_scalarmult_base(self.client_secret_key)

        self.key = crypto_box_beforenm(self.server_public_key, self.client_secret_key)
        self.session_key: bytearray = None
        
        self.nonce = Nonce(keys=[
            self.client_public_key,
            self.server_public_key
        ])
        self.client_nonce = Nonce()
        self.server_nonce: Nonce = None
    
    def encrypt(self, packet_type, payload):
        if packet_type == 10100:
            return payload
        elif packet_type == 10101:
            msg = self.session_key + self.client_nonce.bytes() + payload
            resultbuf = crypto_box_afternm(
                msg,
                self.nonce.bytes(), 
                self.key)
            return self.client_public_key + bytes(resultbuf)
        else:
            self.client_nonce.increment()
            return bytes(crypto_box_afternm(payload, self.client_nonce.bytes(), self.key))
    
    def decrypt(self, packet_type, payload):
        if packet_type == 20100:
            self.session_key = payload[4:28]
            return payload
        elif packet_type in (20104, 20103):
            if not self.session_key:
                return payload

            nonce = Nonce(
                nonce=self.client_nonce.bytes(),
                keys=[
                    self.client_public_key,
                    self.server_public_key
                ]
            )
            
            decrypted = crypto_box_open_afternm(payload, nonce.bytes(), self.key)

            self.server_nonce = Nonce(
                nonce=decrypted[0:24]
            )

            self.key = decrypted[24:56]
            return decrypted[56:]
        else:
            self.server_nonce.increment()
            return crypto_box_open_afternm(payload, self.server_nonce.bytes(), self.key)
