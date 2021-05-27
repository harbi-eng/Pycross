import subprocess
import inspect
import sys
from net import net

class pycross:
    def __init__(self):
        self.message_number=0
        self.interpreters=[]
        self.Proc=[]

    def make_sharedmemory(self,size=2000):
        from SharedMemory import SharedMemory

        self.SharedMemory = SharedMemory(1, size=size)
        self.slavePath = __file__[::-1].replace('pycross.py'[::-1], 'slave.py'[::-1], 1)[::-1]

    def setPyPy(self,path):
        self.pypy = self.meta_decorator(path)

    def setJython(self,path):
        self.Jython = self.meta_decorator(path)

    def setIronPython(self,path):
        self.IronPython = self.meta_decorator(path)

    def setCPython(self,path):
        self.CPpython = self.meta_decorator(path)


    def __is_exist(self,interpreter):
        if interpreter not in self.interpreters:
            self.interpreters.append(interpreter)

            mainFile=sys.argv[0].split("/")[-1]

            self.Proc.append(subprocess.Popen(f'{interpreter} {self.slavePath} {self.SharedMemory.name}'
                                              f' {mainFile} {len(self.interpreters)} {self.SharedMemory.size-self.SharedMemory.META_DATA_SIZE}',
                                              shell=True,stdout=sys.stdout,stderr=sys.stderr,))

    def meta_decorator(self,interpreter_path):
        def decorator(ip=None,port=None):
            def inner_decorator(function):
                def wrapper(*args, **kwargs):
                    if ip is not None and port is not None:
                        self.net = net(1,ip, port)
                        funcName,msg = function.__name__,""
                        func=(funcName,args,kwargs)
                        self.net.send('RF',func)

                        while 1:
                            msg, data = self.net.recv()
                            msg=msg.replace(' ','') # to remove the white space in the msg

                            if msg == "end":
                                return data

                            if msg=="SF":
                                data=func

                            self.net.msgToFunc[msg](data)

                    else:
                        self.__is_exist(interpreter_path)
                        def_line = inspect.getsource(function).split('\n')[1]
                        funcName = def_line[4:def_line.find('(')]
                        self.SharedMemory.send((funcName, args, kwargs),self.message_number,0,
                                               self.interpreters.index(interpreter_path)+1)
                        self.message_number+=1
                        self.SharedMemory.wait()
                        ans = self.SharedMemory.recv()
                        return ans
                return wrapper
            return inner_decorator
        return decorator



    def __del__(self):
        for proc in self.Proc:
            proc.kill()
