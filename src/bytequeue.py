class ByteQueue:
    def __init__(self):
        self._data = None
    
    def add(self, buffer):
        if self._data is None:
            self._data = buffer
        else:
            self._data += buffer

    def get(self):
        return self._data
    
    def size(self):
        return len(self._data)
    
    def release(self, size):
        self._data = self._data[size:]
    
    def reset(self):
        self._data = None
