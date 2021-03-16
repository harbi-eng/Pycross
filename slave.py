# from pycross import SharedMemory
import sys
import re
import os
from net import net
import socket
from SharedMemory import SharedMemory

keywords=['setPyPy']#all the set method from the master class
Pycross=[]          #all of the pycross objects names that the user used in his/her code

with open(sys.argv[2]+'.py') as f:
    buffer =f.read()
    match=re.search('[\s\S]*import\s*pycross',buffer)

    buffer=buffer.replace(match.group(),'').split('\n')

    lines = [[line for line in buffer if key in line] for key in keywords]
    for line_per_key in lines:
        for line in line_per_key:
            obj_name= line.split(".")[0].replace(" ","")
            if obj_name not in Pycross:
                Pycross.append("@"+obj_name)
                Pycross.append(obj_name)

    buf=[]
    for line in buffer:
        for index,obj in enumerate(Pycross):
            if obj in line:
                break
            if index==len(Pycross)-1:
                buf.append(line)


    buf="\n".join(buf)
    file = open('buf.py',"+w")
    file.write(buf)
    file.close()
    exec('from buf import *')
    os.remove('buf.py')




class Slave:
    def __init__(self,ID,name=None):
        self.ID=ID
        if name is not None:
            self.SharedMemory = SharedMemory(0,size=2000,name=name)
        else:
            self.net=net(0,'127.0.1.1',1700)
            self.mainLoop=self.Net


    def Net(self):
        file=self.net.recv()
        print(file)



    def mainLoop(self):
        while 1:
#            headerLength, ID, src, dst, dataLength, data
            _,ID,DST,SRC,_,_=self.SharedMemory.wait()

            funcName,args,kwargs = self.SharedMemory.Read()
            result = globals()[funcName](*args,**kwargs)

            self.SharedMemory.Write(result,ID,SRC,DST)
            break

    def __del__(self):
        try:
            exit(0)
        except Exception as e:
            print(e)
        pass



def runSlave():
    slave=Slave(1,sys.argv[1])
    slave.mainLoop()



runSlave()





