# from pycross import SharedMemory
import sys
import re
from net import net
import socket
from SharedMemory import SharedMemory
from importlib import import_module
import preprocessing

class Slave:
    def __init__(self,ID=1,name=None):
        self.ID=ID
        self.keywords=['setPyPy','pycross()']
        self.Pycross=[]
        self.MainFile=None
        if len(sys.argv)>1:
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
        self.net = net(0, host, 1700)
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
#            headerLength, ID, src, dst, dataLength, data
            Hlen,ID,SRC,DST,MSG=self.SharedMemory.wait()

            funcName,args,kwargs = self.SharedMemory.Read()

            Func = getattr(self.MainFile,funcName)
            result = Func(*args,**kwargs)

            self.SharedMemory.Write(result,ID,self.ID,SRC)
            # break



def runSlave():
    Slave()



runSlave()


