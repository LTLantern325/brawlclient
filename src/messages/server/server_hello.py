from ...bytestream import ByteStream

class ServerHelloMessage:
    packet_type = 20100 # TODO: same as login ok??

    def __init__(self):
        self.bytestream = ByteStream()
    
    def decode(self):
        pass