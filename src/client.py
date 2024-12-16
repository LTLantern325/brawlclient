import socket
import logging
from .crypto import pepper
from . import messages
from . import bytequeue
import struct

def get_default_settings():
    return {
        "hash": "ad243357c65ef991993a73261437c2b0f6aa0d4d",
        "major": 58,
        "minor": 329,
        "build": 1
    }

def _read_uint(b, offset, length, order="big"):
    return int.from_bytes(b[offset:offset+length], order)
def _read_uint16(b, offset, order="big"):
    return _read_uint(b, offset, 2, order)

class Client:
    def __init__(self, settings, remote_addr=("game.brawlstarsgame.com", 9339)):
        self.remote_addr = remote_addr
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.settings = settings
        self.crypto = pepper.PepperCrypto()
        self.queue = bytequeue.ByteQueue()

        self.hi: int = 0
        self.lo: int = 0
        self.token: str = ""

        self._stop_flag = False

        self.handlers = {}

        # default packet handlers
        @self.on_packet(20103)
        def on_login_failed(pkt: messages.server.LoginFailedMessage):
            import json

            if (pkt.error_code != 7):
                raise ConnectionRefusedError(f"LoginFailedMessage: received error code {pkt.error_code}")
            
            data = json.loads(pkt.fingerprint)
            sha, version = data["sha"], data["version"]
            
            logging.info(f"LoginFailedMessage: updating fingerprint settings <hash: {sha}, version: {version}>")
            self.settings["hash"] = sha
            versions = tuple(map(int, version.split(".")))
            self.settings["major"] = versions[0]
            self.settings["minor"] = versions[1]
            self.settings["build"] = versions[2]
            self.flush()
            self.connect() # reconnect
                           # TODO: possible stack overflow?
        
        @self.on_packet(20104)
        def on_login_ok(pkt: messages.server.LoginOkMessage):
            self.hi = pkt.hi
            self.lo = pkt.lo
            self.token = pkt.token
            self.flush()

        @self.on_packet(20100)
        def on_server_hello(pkt: messages.server.ServerHelloMessage):
            self.send_pepper_login()

    def stop(self):
        self._stop_flag = True

    def flush(self):
        logging.warning("!! Some inner code requested settings reflush. Please consider implementing this function by subclassing the client.")
    
    def on_packet(self, packet_type):
        def annotation(func):
            if packet_type not in self.handlers:
                self.handlers[packet_type] = []
            self.handlers[packet_type].append(func)
            return func
        return annotation

    def connect(self):
        self.socket.connect(self.remote_addr)
        self.send_pepper_auth()

        while not self._stop_flag:
            data = self.socket.recv(1024)
            self.queue.add(data)
            while self.pending_job():
                self.update()
    
    def pending_job(self):
        if self.queue.size() < 7:
            return False
        return _read_uint(self.queue.get(), 2, 3) <= self.queue.size() - 7
    
    def dispatch_packet(self, packet_type, packet):
        for handler in self.handlers.get(packet_type, []):
            handler(packet)
    
    def update(self):
        buffer = self.queue.get()
        length = _read_uint(buffer, 2, 3)
        packet_type = _read_uint16(buffer, 0)
        version = _read_uint16(buffer, 5)

        self.queue.release(length + 7)

        payload = self.crypto.decrypt(packet_type, buffer[7:length + 7])

        if payload is None:
            raise ValueError(f"Could not decrypt packet with type {packet_type}")
        
        logging.debug(f"received message of type: {packet_type}, length: {length}, version: {version}")
        
        message = messages.factory.create_message(packet_type)

        if message:
            message.bytestream.set(payload)
            message.decode()
            self.dispatch_packet(packet_type, message)
        else:
            logging.info(f"ignoring unsupported message ({packet_type})")
        
        """if (dump) {
            if (!messages[type]) messages[type] = 0;
            fs.writeFileSync("./PacketsDumps/{}-{}.bin".format(type, messages[type]), payload);
            messages[type] += 1;
        }"""
    
    def send_pepper_auth(self):
        message = messages.client.ClientHelloMessage()
        message.bytestream.set(100)
        message.encode(self)
        self.encrypt_and_write(10100, 0, message.bytestream.getBytes())
    
    def send_pepper_login(self):
        message = messages.client.LoginMessage()
        message.bytestream.set(250)
        message.encode(self)
        self.encrypt_and_write(10101, 0, message.bytestream.getBytes())
    
    def encrypt_and_write(self, packet_type, version, buffer):
        header = bytearray(7)

        struct.pack_into(">H", header, 0, packet_type)

        buffer = self.crypto.encrypt(packet_type, buffer)

        #logging.info([int(i) for i in buffer])

        buffer_length = len(buffer)
        header[2:5] = buffer_length.to_bytes(3, byteorder="big")

        struct.pack_into(">H", header, 5, version)

        self.socket.sendall(header)
        self.socket.sendall(buffer)


        logging.debug(f"Sent message of type: {packet_type}, length: {buffer_length}")
        