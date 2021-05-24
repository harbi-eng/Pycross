import mmap
import struct
import time
import serializer
import string
import random
import posix_ipc
import Messages


class SharedMemory:
    def __init__(self, mode, lock1="LOCK1", lock2="LOCK2", lock3="LOCK3", lock4="LOCK4", size=1024 * 20, name=None):
        self.__Queue = []
        self.mode = mode
        self.META_DATA_SIZE = 52
        self.__MSG_LEN = 20
        self.name = self.__random_name_generator() if name is None else name
        self.__shared_mem_setup(mode, size)
        self.__sem1 = posix_ipc.Semaphore(lock1, posix_ipc.O_CREAT)

        if mode:
            self.__master_init(lock2,lock3,lock4)
        else:
            self.__slave_init(lock2,lock4,lock3)

        self.__functions = {
            'R': self.__recv,
        }
        self.__message = Messages.Messages()

    def __master_init(self,lock2,lock3,lock4):
        self.__sem3 = posix_ipc.Semaphore(lock3, posix_ipc.O_CREAT)
        self.__sem4 = posix_ipc.Semaphore(lock4, posix_ipc.O_CREAT)
        self.__sem2 = posix_ipc.Semaphore(lock2, posix_ipc.O_CREAT)

        self.__sem1.release()
        self.__sem2.release()
        self.__sem3.release()
        self.__sem4.release()

        self.__sem2.acquire()
        self.__sem3.acquire()
        self.__sem4.acquire()


        self.__PTR_READ = 12
        self.__PTR_WRITE = 32
        self.__PTR_HEAD = 4

        self.head = self.META_DATA_SIZE

        self.cap = self.size - self.META_DATA_SIZE

        self.send = self.__master_send
        self.__recv = self.__master_recv
        self.__data_generator = self.__master_data_generator

    def __slave_init(self,lock2,lock3,lock4):
        self.__sem2 = posix_ipc.Semaphore(lock2,posix_ipc.O_RDWR)
        self.__sem3 = posix_ipc.Semaphore(lock3,posix_ipc.O_RDWR)
        self.__sem4 = posix_ipc.Semaphore(lock4,posix_ipc.O_RDWR)

        self.__PTR_READ = 32
        self.__PTR_WRITE = 12
        self.__PTR_HEAD = 8

        self.head = self.size

        self.send = self.__slave_send
        self.__recv = self.__slave_recv
        self.__data_generator = self.__slave_data_generator

    def __random_name_generator(self, size=17):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))

    def wait(self):
        message = self.__read_message()
        self.__functions.get(message[4].replace(" ", ""))()
        return message

    def __shared_mem_setup(self, mode, size):
        flag = (posix_ipc.O_RDWR, posix_ipc.O_CREAT | posix_ipc.O_TRUNC | posix_ipc.O_RDWR)[mode]
        self.size = size + self.META_DATA_SIZE

        if mode:
            self.size = self.size + mmap.PAGESIZE - (self.size % mmap.PAGESIZE)

        shared_mem = posix_ipc.SharedMemory(self.name, flags=flag, size=self.size)
        self.mem = mmap.mmap(shared_mem.fd, self.size, mmap.MAP_SHARED, mmap.PROT_WRITE)
        self.mem.flush()

    def __read_message(self):
        self.__sem3.acquire()

        self.__sem2.acquire()

        msg = self.mem[self.__PTR_READ:self.__PTR_READ + 20]


        if msg != b"\x00" * 20:
            self.mem[self.__PTR_READ:self.__PTR_READ + 20] = b"\x00" * 20
            self.mem.flush()

        return self.__message.unpack(msg)

    def __write_message(self, mess, ID, SRC, DST):
        msg = self.__message.pack(mess, ID, SRC, DST)
        self.mem[self.__PTR_WRITE:self.__PTR_WRITE + len(msg)] = msg
        self.mem.flush()

        self.__sem2.release()

        self.__sem4.release()



    @property
    def cap(self):
        return struct.unpack("<i", self.mem[0:4])[0]

    @cap.setter
    def cap(self, value):
        self.mem[0:4] = struct.pack("<I", value)

    @property
    def head(self):
        return struct.unpack("<I", self.mem[self.__PTR_HEAD:self.__PTR_HEAD + 4])[0]

    @head.setter
    def head(self, value):
        self.mem[self.__PTR_HEAD:self.__PTR_HEAD + 4] = struct.pack("<I", value)

    def __mem_check(self, length):
        if length > self.size - self.META_DATA_SIZE:
            raise Exception(f"the data size {length} is bigger than the shared memory ")

        while self.cap < length:
            with self.__sem1: time.sleep(0.00001)

    def __master_mem_write(self, size_ptr, size, data_ptr, data):
        self.mem[self.head:size_ptr] = size
        self.mem[size_ptr:data_ptr] = data
        self.head = data_ptr

    def __slave_mem_write(self, size_ptr, size, data_ptr, data):
        self.mem[size_ptr:self.head] = size
        self.mem[data_ptr:size_ptr] = data
        self.head = data_ptr

    def __master_send(self, data, ID, SRC, DST):
        data_bytes = serializer.dumps(data)
        size = len(data_bytes)
        size_bytes = struct.pack("<I", size)
        self.__mem_check(size + 4)

        with self.__sem1:
            size_ptr = self.head + 4
            data_ptr = size_ptr + size
            self.__master_mem_write(size_ptr, size_bytes, data_ptr, data_bytes)
            self.cap = self.cap - size - 4
            self.mem.flush()

        self.__write_message('R', ID, SRC, DST)

    def __slave_send(self, data, ID, SRC, DST):
        data_bytes = serializer.dumps(data)
        size = len(data_bytes)
        size_bytes = struct.pack("<I", size)
        self.__mem_check(size + 4)

        with self.__sem1:
            size_ptr = self.head - 4
            data_ptr = size_ptr - size
            self.__slave_mem_write(size_ptr, size_bytes, data_ptr, data_bytes)
            self.cap = self.cap - size - 4
            self.mem.flush()

        self.__write_message('R', ID, SRC, DST)

    def __master_recv(self):
        with self.__sem1:
            slave_head = struct.unpack("<i", self.mem[8:12])[0]
            slave_data = self.mem[slave_head:self.size]

            self.mem[8:12] = struct.pack("<i", self.size)
            self.cap = self.size - self.head + self.META_DATA_SIZE
            self.mem.flush()

        self.__Queue.append(self.__data_generator(slave_data))

    def __slave_recv(self):
        with self.__sem1:
            master_head = struct.unpack("<i", self.mem[4:8])[0]
            master_data = self.mem[self.META_DATA_SIZE:master_head]

            self.mem[4:8] = struct.pack("<i", self.META_DATA_SIZE)
            self.cap = self.head
            self.mem.flush()

        self.__Queue.append(self.__data_generator(master_data))

    @staticmethod
    def __master_data_generator(data):
        INT_SIZE = 4
        end_index = len(data)
        start_index = end_index - INT_SIZE

        while 1:
            try:
                object_bytes = struct.unpack("<I", data[start_index:end_index])[0]

                end_index = start_index
                start_index -= object_bytes
                yield serializer.loads(data[start_index:end_index])
                end_index = start_index
                start_index -= INT_SIZE
            except Exception:
                break

    @staticmethod
    def __slave_data_generator(Data):
        start_index = 0
        end_index = 4
        INT_SIZE = 4

        while 1:
            try:
                object_bytes = struct.unpack("<I", Data[start_index:end_index])[0]
                start_index += INT_SIZE
                end_index = start_index + object_bytes
                yield serializer.loads(Data[start_index:end_index])
                start_index = end_index
                end_index += INT_SIZE
            except Exception:
                break

    def recv(self, arg=0):
        if len(self.__Queue) == 0 or arg:
            self.__read()

        while len(self.__Queue) != 0:
            try:
                return next(self.__Queue[0])

            except Exception:
                self.__Queue.pop(0)

    def __del__(self):
        try:
            self.__sem1.unlink()
            self.__sem2.unlink()
            self.__sem3.unlink()
            self.__sem4.unlink()


            self.__sem1.close()
            self.__sem2.close()
            self.__sem3.close()
            self.__sem4.close()
        except Exception as e:pass



