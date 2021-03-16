from pycross import pycross

PyCross = pycross()
PyCross.make_sharedmemory()
PyCross.setPyPy('/home/void/anaconda3/envs/pypy_env/bin/pypy3')



@PyCross.pypy()
def func1(a,b):
    size:int=10000
    v:list[int] =[0]*size
    v[5000]=0
    Ttotal:float=0.0
    repetation:int=30
    for i in range(repetation):
        for y in range(10):
            for y in range(size-2,0,-1):
                val:int = v[y-1] << 2 | v[y] << 1 | v[y+1]
                v[y] = (val ==3 or val == 5 or val == 6)
    return 11


if __name__ == '__main__':
    func1(4,5)















