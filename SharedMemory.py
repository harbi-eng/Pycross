
import mmap
import struct
import time
import pickle
import string
import random
import posix_ipc
import Messages

class SharedMemory:
    def __init__(self,mode,lock1="voidLock1",lock2="voidLock2",size=1024*20,name=None):
        self.Queue=[]
        self.metaDataSize=62
        if name==None:
            self.name=self.nameGen()
        else:
            self.name=name


        self.SharedMemorySetUp(mode,size,self.name)


        if mode:
            self.sem1 = posix_ipc.Semaphore(lock1, posix_ipc.O_CREAT)
            self.sem2 = posix_ipc.Semaphore(lock2, posix_ipc.O_CREAT)
            self.sem1.release()
            self.sem2.release()
            self.ptr_read=12
            self.ptr_write=37
            self.ptr_head = 4
            self.head = self.metaDataSize
            self.Write = self.__Mwrite
            self.__read = self.__Mread
            self.DataGen = self.__Mdatagen
            self.cap = self.size - self.metaDataSize

        else:
            self.sem1 = posix_ipc.Semaphore(lock1,posix_ipc.O_CREAT)
            self.sem2 = posix_ipc.Semaphore(lock2, posix_ipc.O_CREAT)
            self.ptr_read=37
            self.ptr_write=12
            self.ptr_head = 8
            self.head = self.size
            self.Write = self.__Swrite
            self.__read = self.__Sread
            self.DataGen = self.__Sdatagen


        self.functions = {
            'R': self.__read,
        }

        self.message = Messages.Messages(mode)


    def nameGen(self,size=17):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))

    def wait(self):
        limt=3
        t0=time.time()
        while 1:
            message = self.ReadMessage()
            if message[4] != '\x00\x00\x00\x00':
                break
            if time.time()-t0>limt:
                time.sleep(0.01)
        #     0        1    2    3        4        5
        #headerLength, ID, src, dst, dataLength, data

        self.functions.get(message[4].replace(" ",""))()
        return message


    def SharedMemorySetUp(self,mode,size,name):
        flag = (posix_ipc.O_RDWR, posix_ipc.O_CREAT | posix_ipc.O_TRUNC | posix_ipc.O_RDWR)[mode]

        if mode:
            self.size = size + self.metaDataSize
            self.size=self.size+mmap.PAGESIZE-(self.size%mmap.PAGESIZE)
            self.SharedMemory = posix_ipc.SharedMemory(name, flags=flag, size=self.size)
            self.mem = mmap.mmap(self.SharedMemory.fd, self.size, mmap.MAP_SHARED, mmap.PROT_WRITE)

            self.mem.flush()

        else:
            self.size = size + self.metaDataSize
            self.SharedMemory = posix_ipc.SharedMemory(name, size=self.size)
            self.mem = mmap.mmap(self.SharedMemory.fd, self.size, mmap.MAP_SHARED, mmap.PROT_WRITE)


    def ReadMessage(self):
        with self.sem2:
            msg = self.mem[self.ptr_read:self.ptr_read + 25]
            self.mem[self.ptr_read:self.ptr_read + 25] = b"\x00" * 25
            self.mem.flush()
        return self.message.unpack(msg)

    def WriteMessage(self,mess,ID,SRC,DST):
        msg=self.message.pack(mess,ID,SRC,DST)
        with self.sem2:
            self.mem[self.ptr_write:self.ptr_write + len(msg)] = msg
            self.mem.flush()

    @property
    def cap(self):
        return struct.unpack("<i", self.mem[0:4])[0]

    @cap.setter
    def cap(self, value):

        self.mem[0:4] = struct.pack("<I", value)

    @property
    def head(self):
        return struct.unpack("<I", self.mem[self.ptr_head:self.ptr_head + 4])[0]

    @head.setter
    def head(self, value):
        self.mem[self.ptr_head:self.ptr_head + 4] = struct.pack("<I", value)

    def MemCheck(self, length):
        if length > self.size-self.metaDataSize:
            print(length,self.size)
            raise Exception(f"the data size {length} is bigger than the shared memory ")
        while self.cap < length:
            with self.sem1: time.sleep(0.0001)


    def __Mwrite(self,data,ID,SRC,DST):

        B_data = pickle.dumps(data)
        length = len(B_data)

        B_length = struct.pack("<I", length)
        self.MemCheck(length + 4)

        with self.sem1:
            ptr_end_length = self.head + 4
            ptr_end_data = ptr_end_length + length
            self.mem[self.head:ptr_end_length] = B_length
            self.mem[ptr_end_length:ptr_end_data] = B_data
            self.head = ptr_end_data
            self.cap = self.cap - length - 4
            self.mem.flush()
        with self.sem2:
            self.WriteMessage('R',ID,SRC,DST)

    def __Mread(self):
        with self.sem1:
            slave_head=struct.unpack("<i",self.mem[8:12])[0]
            slave_byte_stream = self.mem[slave_head:self.size]
            self.cap = self.size - self.head + self.metaDataSize

            self.mem[8:12] = struct.pack("<i", self.size)

            self.mem.flush()
        self.Queue.append(self.DataGen(slave_byte_stream))

    def __Mdatagen(self,Data):
        End_index = len(Data)
        Start_index = End_index - 4

        while 1:
            try:
                End_object_bytes = struct.unpack("<I", Data[Start_index:End_index])[0]

                End_index = Start_index
                Start_index -= End_object_bytes
                yield pickle.loads(Data[Start_index:End_index])
                End_index = Start_index
                Start_index -= 4


            except Exception: break

    def __Swrite(self,data,ID,SRC,DST):
        B_data = pickle.dumps(data)
        length = len(B_data)

        B_length = struct.pack("<I", length)

        self.MemCheck(length)

        with self.sem1:
            ptr_end_length = self.head - 4
            ptr_end_data = ptr_end_length - length
            self.cap = self.cap - length - 4
            self.mem[ptr_end_length:self.head] = B_length
            self.mem[ptr_end_data:ptr_end_length] = B_data
            self.head = ptr_end_data
            self.mem.flush()
        with self.sem2:
            self.WriteMessage('R',ID,SRC,DST)


    def __Sread(self):
        with self.sem1:
            head = self.head
            master_head = struct.unpack("<i",self.mem[4:8])[0]
            master_byte_stream = self.mem[self.metaDataSize:master_head]
            self.cap = head

            self.mem[4:8] = struct.pack("<i", self.metaDataSize)
            self.mem.flush()
        self.Queue.append(self.DataGen(master_byte_stream))

    def __Sdatagen(self,Data):
        Start_index = 0
        End_index = 4

        while 1:
            try:
                End_Byte_object = struct.unpack("<I", Data[Start_index:End_index])[0]
                Start_index += 4
                End_index = Start_index + End_Byte_object
                yield pickle.loads(Data[Start_index:End_index])
                Start_index = End_index
                End_index += 4
            except Exception: break

    def Read(self,arg=0):
        if len(self.Queue)==0 or arg:
            self.__read()

        while len(self.Queue) !=0:
            try:
                return next(self.Queue[0])

            except Exception:self.Queue.pop(0)




