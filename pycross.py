from SharedMemory   import  *
from Sharedmessages import *
import subprocess
import inspect
import sys
from net import net


class pycross:
    def __init__(self):
        self.message_number=0

    def make_sharedmemory(self,size=2000):
        self.SharedMemory = SharedMemory(1, size=size)
        self.slavePath = __file__[::-1].replace('pycross.py'[::-1], 'slave.py'[::-1], 1)[::-1]
        self.interpreters=[]
        self.Proc=[]

    def setPyPy(self,path):
        self._pypy=path




    def __is_exist(self,interpreter):
        if interpreter not in self.interpreters:
            self.interpreters.append(interpreter)
            self.Proc.append(subprocess.Popen(f'{interpreter} {self.slavePath} {self.SharedMemory.name} {sys.argv[0].split("/")[-1].replace(".py","")} {len(self.interpreters)+1}',shell=True,stdout=sys.stdout,stderr=sys.stderr,))
            # print('\n')
            # self.SharedMemory.Write(globals().copy())
            # time.sleep(1)


    def pypy(self,ip=None,port=None):
        def inner_pypy(function):
            def wrapper(*args, **kwargs):
                if ip is not None and port is not None:
                    self.net = net(1, ip, port)
                    print(function.__name__)

                    funcName = inspect.getsource(function).split()[2][:-5]
                    self.net.send((funcName, args, kwargs))
                else:
                    self.__is_exist(self._pypy)
                    funcName = inspect.getsource(function).split()[2][:-6]
                    print(args,kwargs)
                    self.SharedMemory.Write((funcName, args, kwargs),self.message_number,0,self.interpreters.index(self._pypy)+1)
                    self.message_number+=1

                    self.SharedMemory.ReadMessage()

                    self.SharedMemory.wait()

                    ans = self.SharedMemory.Read()

            return wrapper
        return inner_pypy



    def __del__(self):
        for proc in self.Proc:
            proc.kill()

    def Resize(self,size):
        self.SharedMemory.Resize(size)

#
#
# class Slave:
#     def __init__(self,name):
#         self.SharedMemory = SharedMemory(0,size=2000,name=name)
#         # globals()[:]=self.SharedMemory.Read()
#         # print(globals())
#         # time.sleep(1)
#
#     def mainLoop(self):
#         while 1:
#             self.SharedMemory.wait()
#
#             funcName,args,kwargs = self.SharedMemory.Read()
#             result = globals()[funcName](*args,**kwargs)
#
#             self.SharedMemory.Write(result)
#
#
# def runSlave(name):
#     slave=Slave(name)
#     slave.mainLoop()
#




#
# def func1():
#     size:int=10000
#     v:list[int] =[0]*size
#     v[5000]=num
#     Ttotal:float=0.0
#     repetation:int=30
#     for i in range(repetation):
#         T0:float=time.time()
#         for y in range(10):
#             for y in range(size-2,0,-1):
#                 val:int = v[y-1] << 2 | v[y] << 1 | v[y+1]
#                 v[y] = (val ==3 or val == 5 or val == 6)
#         Ttotal+=time.time()-T0
#     return 123
#
# def func2():
#     size:int=10000
#     v:list[int] =[0]*size
#     v[5000]=num
#     Ttotal:float=0.0
#     repetation:int=30
#     for i in range(repetation):
#         T0:float=time.time()
#         for y in range(10):
#             for y in range(size-2,0,-1):
#                 val:int = v[y-1] << 2 | v[y] << 1 | v[y+1]
#                 v[y] = (val ==3 or val == 5 or val == 6)
#         Ttotal+=time.time()-T0
#     return 1234
#



#
# if __name__ =="__main__":
#     args=sys.argv
#     if len(args) ==1:
#
#         master = Master()
#         TotalTime=0
#         master.run(func1,"/home/void/anaconda3/envs/pypy_env/bin/pypy3")
#
#         print("one done")
#         master.run(func2,"/home/void/anaconda3/envs/pypy_env/bin/pypy3")
#         print("two done")
#
#     else:
#         sub(sys.argv[1])















































