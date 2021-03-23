from pycross import pycross
import socket

PyCross = pycross()
PyCross.make_sharedmemory(100208)
PyCross.setPyPy('/home/void/anaconda3/envs/pypy_env/bin/pypy3')

HOST = socket.gethostbyname(socket.gethostname())
PORT = 1700

@PyCross.pypy()
def func1():
    size:int=100000
    v:list[int] =[0]*size
    v[size//2]=1
    Ttotal:float=0.0
    repetation:int=30
    for i in range(repetation):
        for y in range(10):
            for y in range(size-2,0,-1):
                val:int = v[y-1] << 2 | v[y] << 1 | v[y+1]
                v[y] = (val ==3 or val == 5 or val == 6)
    return v


if __name__ == '__main__':
    ans=func1()
    print(ans)
