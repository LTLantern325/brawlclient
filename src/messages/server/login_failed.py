from ...bytestream import ByteStream

class LoginFailedMessage:
    packet_type = 20103

    def __init__(self):
        self.bytestream = ByteStream()

        self.error_code: int
        self.fingerprint: str
    
    def decode(self):
        self.error_code = self.bytestream.readInt()
        self.fingerprint = self.bytestream.readString()
