from ...bytestream import ByteStream

class ClientHelloMessage:
    def __init__(self):
        self.bytestream = ByteStream()
    
    def encode(self, client):
        self.bytestream.writeInt(2) # protocol version
        self.bytestream.writeInt(47) # crypto version
        self.bytestream.writeInt(client.settings["major"]) # major version
        self.bytestream.writeInt(client.settings["build"]) # build version
        self.bytestream.writeInt(client.settings["minor"]) # minor version
        self.bytestream.writeString(client.settings["hash"]) # master hash
        self.bytestream.writeInt(0)
        self.bytestream.writeInt(0)