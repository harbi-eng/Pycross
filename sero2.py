import struct
import cProfile,pstats
"""
everything will be inside a list
we have two type of things to serilize

1)str,int,float, boolean 
2)list,dict,tuple
if it was from the first type, then use struct streat a head
if it was from the second type, then we are going to make a buffer(list) of bytes


so i have List, tuple, dict, object, 
i need a byte at the start of the buffer to identfiy the type of the continer
then start putting the data inside, if i had list inside a list? 
then i need to say where to start and where to end

why not making the buffer a dict of lists
what the advantages? hmmm None, then don't do it


"""

"""
byte    meaning
0       None
1       bool
2       int
3       float
4       string
5       list
6       tuple
7       dict

"""

Buff=[]
import io

def profile(func):
    def inner(*args,**kwargs):
        pr=cProfile.Profile()
        pr.enable()
        retval = func(*args,**kwargs)
        pr.disable()
        s=io.StringIO()
        sortby = 'cumulative'
        ps=pstats.Stats(pr,stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
        return retval
    return inner




def NoneSero(obj):
    global Buff
    Buff.append(b'0')

def BoolSero(obj):
    global Buff
    Buff.append(b'1')
    Buff.append(struct.pack('<?',obj))

def IntSero(obj):
    global Buff
    Buff.append(b'2')
    Buff.append(struct.pack('<i',obj))

def FloatSero(obj):
    global Buff
    Buff.append(b'3')
    Buff.append(struct.pack('<f',obj))

def StrSero(obj):
    global Buff

    Buff.append(b''.join([b'4',obj.encode()]))

def ListSero(List):
    global Buff

    switcher = {
        bool:   (b'1','<?'),
        int:    (b'2','<i'),
        float:  (b'3','<f'),
        str:    (b'4','<s'),
        list: ListSero,
    }

    Buff.append(b'5')
    for value in List:
        _type=type(value)
        _byte,sign=switcher.get(_type)
        Buff.append(_byte+struct.pack(sign,value))

    Buff.append(b'5')

def sero(obj):

    switcher = {
        bool: BoolSero,
        int: IntSero,
        float: FloatSero,
        str: StrSero,
        list: ListSero,
    }

    switcher.get(type(obj))(obj)
    return Buff



import random,string
List=[]*10000000

for num in range(10000000):
    if num%4==1:
        List.append(random.randint(0,100000))
    elif num%4==2:
        List.append(random.uniform(1.5,1.9))
    elif num%4==3:
        List.append(bool(random.randint(0,2)))
    else:
        List.append("".join( [random.choice(string.ascii_letters) for i in range(random.randint(1,12))]))

import time

td = time.time()

sero(List)
print(time.time()-td)






