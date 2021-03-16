import struct
import mmap
import time

class Messages:
    def __init__(self,mode):#message max size = 5 bytes
        # shared memory
        self.mode=mode
        self.b_len = 20

        if mode:
            self.ptr_read=12
            self.ptr_write=37
        else:
            self.ptr_read=37
            self.ptr_write=12

    def pack(self, data, ID, src, dst):

        ID  = struct.pack('<i', ID)
        src = struct.pack('<i', src)
        dst = struct.pack('<i', dst)
        headerLength = struct.pack('<i', self.b_len)

        dataBytes = struct.pack(f'{len(data)}s', data.encode())  # .encode()
        dataLength = struct.pack('<i', len(dataBytes))

        return headerLength + ID +src +dst +dataLength+dataBytes


    def unpack(self,msg):
        headerLength = struct.unpack('<i', msg[:4])[0]
        ID = struct.unpack('<i', msg[4:8])[0]
        src = struct.unpack('<i', msg[8:12])[0]
        dst = struct.unpack('<i', msg[12:16])[0]
        dataLength = struct.unpack('<i', msg[16:20])[0]
        if dataLength==0:
            return b'\x00'

        data = msg[20:20+dataLength].decode()

        return headerLength, ID, src, dst, dataLength, data