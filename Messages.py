import struct
import serializer

class Messages:
    def __init__(self,mode):
        self.mode=mode
        self.msg_len=4

        if mode:
            self.ptr_read=12
            self.ptr_write=37
        else:
            self.ptr_read=37
            self.ptr_write=12


    def pack(self, msg, ID, src, dst,data=None):
        ID  = struct.pack('<i', ID)
        src = struct.pack('<i', src)
        dst = struct.pack('<i', dst)
        msg+=" "*(self.msg_len-len(msg))

        msgBytes = msg.encode()  # .encode()
        if data is None:
            headerLength = struct.pack('<i', 20)    #in case data is None, the header len is 20
            packed=headerLength + ID + src + dst + msgBytes
            return packed

        headerLength = struct.pack('<i', 24)    #in case data is not None, the header len is 24

        dataBytes  = serializer.dumps(data)
        dataLength = struct.pack('<i', len(dataBytes))

        packed=headerLength + ID +src +dst +msgBytes+dataLength+dataBytes
        return packed

    def unpack(self,packet):
        headerLength = struct.unpack('<i', packet[0:4])[0]
        ID = struct.unpack('<i', packet[4:8])[0]
        src = struct.unpack('<i', packet[8:12])[0]
        dst = struct.unpack('<i', packet[12:16])[0]
        msg = packet[16:20].decode().replace(" ","")

        if headerLength==0:
            return '\x00'

        if headerLength==20:
            return headerLength, ID, src, dst, msg

        dataLength = struct.unpack('<i', packet[20:24])[0]
        return headerLength, ID, src, dst, msg,dataLength

