import sys
from net import net
import socket
from importlib import import_module
import preprocessing
from std_overwrite import output,error



class Slave:
    def __init__(self,ID=1,name=None):
        self.ID=ID
        self.keywords=['setPyPy','pycross()']
        self.Pycross=[]
        self.MainFile=None
        if len(sys.argv)>1:
            from SharedMemory import SharedMemory
            self.ID=int(sys.argv[3])
            self.SharedMemory = SharedMemory(0,size=int(sys.argv[4]),name=sys.argv[1])
            self.FileSetUp()
            self.mainLoop()

        self.mainNet()

    def FileSetUp(self):
        with open(sys.argv[2],"r") as file:
            preprocessing.filesetup(self.keywords,file.read())
        self.MainFile = import_module('MainFile')

    def mainNet(self):
        host = socket.gethostbyname(socket.gethostname())


        self.net = net(0, host, 1701)

        stdout = output(self.net)
        stderr = error(self.net)

        sys.stdout = stdout
        sys.stderr = stderr

        while 1:
                msg, data = self.net.recv()
                msg=msg.replace(' ','') #remove white spaces from the message

                if len(msg):
                    end=self.net.msgToFunc[msg](data)

                if end:
                    break

                self.net.socket.close()
                self.net.socket.close()


    def mainLoop(self):
        while 1:
            data=self.SharedMemory.wait()
            Hlen,ID,SRC,DST,MSG = data
            funcName,args,kwargs = self.SharedMemory.recv()
            Func = getattr(self.MainFile,funcName)
            result = Func(*args,**kwargs)

            self.SharedMemory.send(result,ID,self.ID,SRC)



def runSlave():
    Slave()



runSlave()


