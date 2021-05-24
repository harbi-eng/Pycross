import socket
import re
import serializer
from Messages import Messages
from importlib import import_module
import os
import preprocessing
import sys


"""
required messages:
      # 1)send function     ->SF
        2)send main file    ->SMF
        3)send packages     ->SP

        5)read function     ->RF
        6)read main file    ->RMF
        7)read packages     ->RP
        
        8)read output       ->RO
        9)read error        ->RE

"""


class net:
    def __init__(self, mode, ip, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.msg = Messages(not mode)
        self.missing_packages = []
        self.keywords = ['setPyPy','pycross()']
        self.Pycross = []

        self.MainFile = None

        if mode:
            self.socket.connect((ip, port))
            self.send = self.__client_send
            self.recv = self.__client_recv

        else:
            self.socket.bind((ip, port))
            self.socket.listen(2)
            self.send = self.__server_send
            self.recv = self.__server_recv
            self.clinet = self.socket.accept()[0]

        self.msgToFunc = {
            "SF": self.sendFunc,
            "RF": self.readFunc,
            "RMF": self.readMainFile,
            "RP": self.readPackages,
            "SMF": self.sendMainFile,
            "SP": self.sendPackages,
            "RO": self.readOutput,
            "RE": self.readError,
            "end": None
        }

    def __del__(self):
        if self.MainFile is not None:
            os.remove('MainFile.py')
            for package in self.missing_packages:
                os.remove(f'{package}.py')

    def sendOutput(self,message):
        self.send("RO",message)


    def readOutput(self,message):
        print(message)

    def sendError(self,error):
        self.send("RE",error)


    def readError(self,error):
        sys.stderr.write(str(error))


    def sendFunc(self, func):
        self.send("RF", func)

    def readFunc(self, func):
        if self.MainFile == None:
            self.send("SMF", "")
            return

        funcName, args, kargs = func
        func = getattr(self.MainFile, funcName)
        result = func(*args, **kargs)
        self.send('end', result)
        return True

    def readMainFile(self, code=None):
        if code is not None:
            code = preprocessing.filesetup(self.keywords,code)
        try:
            self.MainFile = import_module('MainFile')
            self.send('SF', '')

        except ModuleNotFoundError:
            packages = self.FindPackages(code)
            self.send('SP', packages)

    def readPackages(self, packages):
        for packageName, packageCode in packages:
            with open(f"{packageName}.py", "w") as file:
                file.write(packageCode)
                file.close()
        self.readMainFile()

    def sendMainFile(self, _=None):
        with open(sys.argv[0], 'r') as file:
            self.send('RMF', file.read())
            file.close()

    def sendPackages(self, packages):
        packages_code = []
        for package in packages:
            with open(f"{package}.py", "r") as file:
                packages_code.append((package, file.read()))
                file.close()

        self.send("RP", packages_code)

    def readResult(self, _=None):
        return self.recv()

    def recvall(self, scoket, msglen=4):
        buffer = b""
        while len(buffer) < msglen:
            packet = scoket.recv(msglen - len(buffer))
            if not packet:
                return None
            buffer += packet
        return buffer

    def __client_send(self, msg, data):
        data = self.msg.pack(msg, 12, 1, 0, data)  # ID  src  dst
        self.socket.sendall(data)

    def __client_recv(self):
        header = self.recvall(self.socket, 24)
        if not header:
            return None

        _, ID, src, dst, msg, dataLength = self.msg.unpack(header)
        data = self.recvall(self.socket, dataLength)
        return msg, serializer.loads(data)

        # server

    def __server_send(self, msg, data):
        data = self.msg.pack(msg, 30, 0, 1, data)  # ID  src  dst
        self.clinet.sendall(data)

    def __server_recv(self):
        header = self.recvall(self.clinet, 24)
        if not header:
            return None

        _, ID, src, dst, msg, dataLength = self.msg.unpack(header)
        data = self.recvall(self.clinet, dataLength)

        return msg, serializer.loads(data)

    def FindPackages(self, code):
        lines = code.split('\n')
        imports = [line for line in lines if 'import' in line]
        matches = [re.search('(?<=from)\s*\w*', line) if 'from' in line else re.search('(?<=import)\s*\w*', line) for
                   line in imports]
        packages = [match.group(0).replace(' ', '') for match in matches]
        self.missing_packages=[]
        for pack in packages:
            try:
                exec(f'import {pack}')
            except ModuleNotFoundError as e:
                self.missing_packages.append(pack)
        return  self.missing_packages


























