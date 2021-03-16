import multiprocessing
import threading
import mmap
import struct
import time
import posix_ipc
import ilock

class SharedMessages:
    def __init__(self,mode,lock="SharedMessagesLock0", name1="Box00"):
        self.lock = ilock.ILock(lock)

        flag = (posix_ipc.O_RDWR, posix_ipc.O_CREAT | posix_ipc.O_TRUNC | posix_ipc.O_RDWR)[mode]
        self.mem = posix_ipc.SharedMemory(name1, flags=flag, size=6)
        self.mem = mmap.mmap(self.mem.fd, self.mem.size, mmap.MAP_SHARED, mmap.PROT_WRITE)


        if mode:
            self.lenptr      = 3
            self.ReadFrom    = 1
            self.WriteTo     = 4
        else:
            self.ReadFrom    = 4
            self.WriteTo     = 1
            self.lenptr      = 0


        self.empty=bytes("\x00",encoding="utf-8")

    def send(self,msg):
        length = len(msg)
        msgBytes = struct.pack(f'<{length}s', msg.encode())
        Blength=struct.pack('<B', length)

        with self.lock:
            self.mem[self.lenptr:self.lenptr+1]=Blength
            self.mem[self.WriteTo:self.WriteTo+length]=msgBytes

    def recv(self):

        length = struct.unpack("<B",self.mem[self.ReadFrom-1:self.ReadFrom] )[0]

        if length ==0:
            return
        msg = struct.unpack(f"<{length}s",self.mem[self.ReadFrom:self.ReadFrom+length])[0].decode()
        with self.lock:
            self.mem[self.ReadFrom-1:self.ReadFrom]=self.empty


        return msg

