"""module.exports = class {
    constructor(obj) {
        this.payload = new Uint8Array(obj);
        this.offset = 0;
    }
    set(obj) {
        this.payload = new Uint8Array(obj);
    }
    write(a1) {
        this.payload[this.offset++] = a1;
    }
    read() {
        return this.payload[this.offset++];
    }
    writeUInt(a1) {
        this.write(a1 & 0xFF);
    }
    writeByte(a1) {
        this.write(a1);
    }
    writeBoolean(a1) {
        this.write(a1 ? 1: 0);
    }
    writeInt(a1) {
        this.write((a1 >> 24) & 0xFF);
        this.write((a1 >> 16) & 0xFF);
        this.write((a1 >> 8) & 0xFF);
        this.write(a1 & 0xFF);
    }
    writeString(a1) {
        if (!a1) return this.writeInt(-1);
        let b = new Uint8Array(Buffer.from(a1));
        this.writeInt(b.length);
        for (let strOffset = 0; strOffset < b.length; strOffset++) {
            this.write(b[strOffset]);
        }
    }
    writeVInt(a1) {
        let v1 = (((a1 >> 25) & 0x40) | (a1 & 0x3F)), 
        v2 = ((a1 ^ (a1 >> 31)) >> 6), v3
       
        a1 >>= 6;
        if (v2 == 0) {
            this.writeByte(v1);
        } else {
            this.writeByte(v1 | 0x80);
            v2 >>= 7;
            v3 = 0;
            if (v2 > 0) {
                v3 = 0x80;
            }
            this.writeByte((a1 & 0x7F) | v3);
            a1 >>= 7;
            while (v2 != 0) {
                v2 >>= 7;
                v3 = 0;
                if (v2 > 0) {
                    v3 = 0x80;
                }
                this.writeByte((a1 & 0x7F) | v3);
                a1 >>= 7;
            }
        }
    }
    writeDataReference(a1, a2) {
        this.writeVInt(a1);
        if (a1 == 0) return;
        this.writeVInt(a2);
    }
    readDataReference() {
        let a1 = this.readVInt();
        return [a1, a1 == 0 ? 0 : this.readVInt()];
    }
    readInt() {
        return (this.read() << 24 | this.read() << 16 | this.read() << 8 | this.read());
    }
    readByte() {
        return this.read();
    }
    readBytes(size) {
        let result = new Uint8Array(size);
        for (let index = 0; index < size; index++) {
            result[index] = this.readByte();
        }
        return result;
    }
    readBoolean() {
        return Boolean(this.read());
    }
    readString() {
        let len = this.readInt();
        if (len <= 0 || len == 4294967295) {
            return "";
        }
        return Buffer.from(this.readBytes(len)).toString();
    }
    readVInt() {
        // this method is discovered by nameless#1347
        let result = 0,
        shift = 0, b, seventh, msb, n;

        while (true) {
            b = this.read();
            if (shift == 0) {
                seventh = (b & 0x40) >> 6;
                msb = (b & 0x80) >> 7;
                n = b << 1;
                n = n & ~0x181;
                b = n | (msb << 7) | seventh;
            }
            result |= (b & 0x7f) << shift;
            shift += 7;
            if ((b & 0x80) <= 0) {
                break;
            }
        }
        return (result >> 1) ^ (-(result & 1));
    }
    getBytes() {
        return this.payload.slice(0, this.offset);
    }
}
"""

class ByteStream:
    def __init__(self):
        self.payload = bytearray()
        self.offset = 0
    
    def set(self, data: bytes | bytearray):
        self.payload = bytearray(data)
    
    def write(self, a1: int):
        self.payload[self.offset] = a1
        self.offset += 1

    def read(self):
        rv = self.payload[self.offset]
        self.offset += 1
        return rv
    
    def writeUInt(self, a1: int):
        self.write(a1 & 0xFF)
    
    def writeByte(self, a1: int):
        self.write(a1)
    
    def writeBoolean(self, a1: bool):
        self.write(1 if a1 else 0)
    
    def writeInt(self, a1: int):
        self.write((a1 >> 24) & 0xFF)
        self.write((a1 >> 16) & 0xFF)
        self.write((a1 >> 8) & 0xFF)
        self.write(a1 & 0xFF)
    
    def writeString(self, a1: str = None):
        if not a1:
            return self.writeInt(-1)
        
        b = bytearray(a1.encode())
        self.writeInt(len(b))
        
        for str_offset in range(len(b)):
            self.write(b[str_offset])
    
    def writeVInt(self, a1: int):
        v1 = (((a1 >> 25) & 0x40) | (a1 & 0x3F))
        v2 = ((a1 ^ (a1 >> 31)) >> 6)
        v3 = 0
       
        a1 >>= 6
        if v2 == 0:
            self.writeByte(v1)
        else:
            self.writeByte(v1 | 0x80)
            v2 >>= 7
            if v2 > 0:
                v3 = 0x80
            self.writeByte((a1 & 0x7F) | v3)
            a1 >>= 7
            while v2 != 0:
                v2 >>= 7
                v3 = 0
                if v2 > 0:
                    v3 = 0x80
                self.writeByte((a1 & 0x7F) | v3)
                a1 >>= 7
    
    def writeDataReference(self, a1: int, a2: int):
        self.writeVInt(a1)
        if a1 == 0:
            return
        
        self.writeVInt(a2)

    def readDataReference(self):
        a1 = self.readVInt()
        return a1, 0 if a1 == 0 else self.readVInt()
    
    def readInt(self):
        return (self.read() << 24 | self.read() << 16 | self.read() << 8 | self.read())
    
    def readByte(self):
        return self.read()
    
    def readBytes(self, size: int):
        result = bytearray()
        for _ in range(size):
            result.append(self.readByte())

        return result
    
    def readBoolean(self):
        return bool(self.read())
    
    def readString(self):
        length = self.readInt()
        if length <= 0 or length == 4294967295:
            return ""
        return self.readBytes(length).decode()
    
    def readVInt(self):
        result = 0
        shift = 0
        b = 0
        seventh = 0
        msb = 0,
        n = 0

        while True:
            b = self.read()
            if shift == 0:
                seventh = (b & 0x40) >> 6
                msb = (b & 0x80) >> 7
                n = b << 1
                n = n & ~0x181
                b = n | (msb << 7) | seventh
            
            result |= (b & 0x7f) << shift
            shift += 7
            if ((b & 0x80) <= 0):
                break
        return (result >> 1) ^ (-(result & 1));
    
    def getBytes(self):
        # TODO: why offset is there??? looks weird but okay
        return bytes(self.payload[:self.offset])