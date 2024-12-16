from ...bytestream import ByteStream

class LoginOkMessage:
    packet_type = 20104 # TODO: same as server hello in orig? i changed it to 20104 here

    def __init__(self):
        self.bytestream = ByteStream()

        self.hi: int
        self.lo: int
        self.token: str
    
    def decode(self):
        self.hi = self.bytestream.readInt()
        self.lo = self.bytestream.readInt()
        self.bytestream.readInt() # TODO: what?
        self.bytestream.readInt()
        self.token = self.bytestream.readString()