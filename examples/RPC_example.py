from pycross import pycross
import socket
PyCross = pycross() #create the pycross object

HOST = socket.gethostbyname(socket.gethostname())  # The server's hostname or IP address
PORT = 1700    # The port used by the server
@PyCross.pypy(HOST,PORT) #decorate the target function with the pypy decorator
def func1():
    size=100
    numbers=[[j for j in range(size)] for _ in range(size)]

    for i in range(size):
        for j in  range(size):
            numbers[i][j]=numbers[j][i]**numbers[i][j]

    return numbers


if __name__ == '__main__': #this is a must for the pycross module to be used
    ans=func1()
    print(ans)