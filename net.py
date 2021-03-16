import socket
import inspect
import  re
import pickle
import sys


"""
so the net must work as follows:
    1)the clinet will send his file to the server
    2)the server will check if all the packages are avaliable           DONE
        1)if he has him then go to 3
        2)else ask the clinet to send you the remining packages
        3)the clinet send the packages back to the server
    3)excute the clinet source code
    4)send the results to the clinet

the question here is it better to modfiy on top of the pycross file? or do i have 
write the code somewhere else then i add it to the pycross? well i am more fan for the later 


so now wut? 


1)deal with the import problem
    1)check all the packages
    2)if you have the package then use it
    3)else connect back the client to take these packages
"""

###this is will be provided by the user

HOST = socket.gethostbyname(socket.gethostname())  # The server's hostname or IP address
PORT = 1700      # The port used by the server

class net:
    def __init__(self,mode,ip,port):
        self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if mode:
            self.socket.connect((ip,port))
            self.send=  self.__c_send
            self.recv = self.__c_recv
            with open(sys.argv[0]) as file:
                data=file.read()
                self.socket.sendall(pickle.dumps(data))
        else:
            self.socket.bind((ip,port))
            self.send=  self.__s_send
            self.recv = self.__s_recv
            self.clinets=None

    def __c_send(self,data):
        self.socket.sendall(pickle.dumps(data))

    def __c_recv(self):
        return pickle.loads(self.socket.recv(1000))

    def __s_send(self,data):
        self.clinets[0].sendall(pickle.dumps(data))


    def __s_recv(self):
        self.socket.listen()
        self.clinets=self.socket.accept()
        with self.clinets[0]:
            return pickle.loads(self.clinets[0].recv(1000))

    def extract_packages(self,data):
        lines = data.split('\n')
        imports = [line for line in lines if 'import' in line]
        matches = [re.search('(?<=from)\s*\w*', line) if 'from' in line else re.search('(?<=import)\s*\w*', line) for
                   line in imports]
        packages = [match.group(0).replace(' ', '') for match in matches]
        request_packages = []
        for pack in packages:
            try:
                exec(f'import {pack}')
            except ModuleNotFoundError as e:
                request_packages.append(pack)






















# def func1():
#     size:int=10000
#     v:list[int] =[0]*size
#     v[5000]=0
#     Ttotal:float=0.0
#     repetation:int=30
#     for i in range(repetation):
#         for y in range(10):
#             for y in range(size-2,0,-1):
#                 val:int = v[y-1] << 2 | v[y] << 1 | v[y+1]
#                 v[y] = (val ==3 or val == 5 or val == 6)
#     return 11
# func= inspect.getsource(func1)

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.connect((HOST, PORT))
#     f = open('net.py')
#     s.sendall(f.read().encode())
#     data = s.recv(1024)

# print('Received', repr(data))












