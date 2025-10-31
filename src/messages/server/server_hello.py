from ...bytestream import ByteStream

class ServerHelloMessage:
    packet_type = 20100

    def __init__(self):
        self.bytestream = ByteStream()
        self.pass_token: bytes = b''  # 패스 토큰을 저장할 변수 추가
    
    def decode(self):
        self.pass_token = self.bytestream.readBytes(32)  # 32바이트 패스 토큰 읽기