from pycross import pycross

PyCross = pycross() #create the pycross object

PyCross.make_sharedmemory(size=8614587)#create the shared memory with the wanted size

PyCross.setPyPy(path='/home/void/anaconda3/envs/pypy_env/bin/pypy3')#set the pypy path

@PyCross.pypy() #decorate the target function with the pypy decorator
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
