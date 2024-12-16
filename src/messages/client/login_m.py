from ...bytestream import ByteStream

class LoginMessage:
    def __init__(self):
        self.bytestream = ByteStream()
    
    def encode(self, client):
        self.bytestream.writeInt(client.hi or 0) # high
        self.bytestream.writeInt(client.lo or 0) # low
        self.bytestream.writeString(client.token) # token

        self.bytestream.writeInt(client.settings["major"])
        self.bytestream.writeInt(client.settings["build"])
        self.bytestream.writeInt(client.settings["minor"])
        self.bytestream.writeString(client.settings["hash"])

        self.bytestream.writeString()
        self.bytestream.writeDataReference(1, 0)
        self.bytestream.writeString("en-US")
        self.bytestream.writeString()
        self.bytestream.writeBoolean(False)
        self.bytestream.writeString()
        self.bytestream.writeString()
        self.bytestream.writeBoolean(True)
        self.bytestream.writeString()
        self.bytestream.writeInt(1448)
        self.bytestream.writeVInt(0)
        self.bytestream.writeString()

        self.bytestream.writeString()
        self.bytestream.writeString()
        self.bytestream.writeVInt(0)

        self.bytestream.writeString()
        self.bytestream.writeString()
        self.bytestream.writeString()

        self.bytestream.writeString()

        self.bytestream.writeBoolean(False)
        self.bytestream.writeString()
        self.bytestream.writeString()