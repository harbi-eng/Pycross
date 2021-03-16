"""

way slower than pickle, and takes way more memory, but can serilaze everything

needs improvement


meaning sign
None    'ᐰ'
bool    'ᐱ'
int     'ᐲ'
float   'ᐳ'
str     'ᐴ'
'       'ᐿ'
_object      'ᐵ'
,       'ᐶ'
{       'ᐷ'
}       'ᐸ'
[       'ᐹ'
]       'ᐺ'
(       'ᐻ'
)       'ᐼ'
:       'ᐽ'


"""
import struct

replacment=['None','bool' ,'int' ,'float' ,'str'   ,'\"'  ,'_object'  ,','  ,'{' ,'}' ,'[' ,']' ,'(' ,')' ,':']
signs=     ['ᐰ'  ,'ᐱ'    , 'ᐲ' ,    'ᐳ' ,   'ᐴ'  ,'ᐿ'   ,'ᐵ'   ,'ᐶ'  ,'ᐷ','ᐸ'  ,'ᐹ','ᐺ' ,'ᐻ','ᐼ' ,'ᐽ']

def Loads(data):
    global signs,replacment
    data=data.decode()
    for s,r in zip(signs,replacment):
        if s in data:
            data=data.replace(s,r)
    return eval(data[:-1])

class obj:
    pass

obj = type("obj",(),{})



def _object(dict):
    global classesDict
    _type=dict['className']
    if _type not in classesDict.keys():
        classesDict[_type] =  type(f"slave_{_type}",(globals()[_type],),{"__init__":func})
    ob=classesDict[_type]()
    ob.__dict__=dict.copy()



    return ob

classesDict={}



def func(self):
    pass


class person(object):
    def __init__(self,name,color,age,hoby):
        self.name = name
        self.age = age
        self.color = color
        self.hoby = hoby

    def changeName(self,name):
        self.name = name
        
    def __getter


class shope():
    def __init__(self,person, shape,size,location):
        self.person=person
        self.shape=shape
        self.size=size
        self.location=location


class twon:
    def __init__(self,name,person,shope,contry,somethingelse):
        self.name=name
        self.someone=person
        self.shope=shope
        self.contry=contry
        self.somethingelse=somethingelse


def simpleSerilazation(_type,obj):
    return f"{_type}ᐻ{obj}ᐼᐶ"

def NoneSerilazation(_type,obj):
    return f"{obj}ᐶ"


def strSerilazation(_type,obj):
    return f"ᐴᐻᐿ{obj}ᐿᐼᐶ"


def seroObjects(retV,obj):
    retV=f'ᐵᐻᐷ ᐴᐻᐿclassNameᐿᐼᐽᐴᐻᐿ{obj.__class__.__name__}ᐿᐼᐶ {retV}'
    for key,value in obj.__dict__.items():
        Vtype, VSeroFunc = ser_switch(value)
        Ktype, KSeroFunc = ser_switch(key)
        retV=f'{retV}{KSeroFunc(Ktype,key)[:-1]}ᐽ{VSeroFunc(Vtype,value)} '
    retV=f'{retV}ᐸᐼᐶ'
    return retV


def seroDict(retV,dict):
    retV=f'ᐷ{retV}'
    for key,value in dict.items():
        Vtype, VSeroFunc = ser_switch(value)
        Ktype, KSeroFunc = ser_switch(key)

        retV=f'{retV}{KSeroFunc(Ktype,key)[:-1]}ᐽ{VSeroFunc(Vtype,value)} '
    retV=f'{retV}ᐸᐶ'
    return retV

def seroList(retV,List):
    retV=f'ᐹ{retV}'
    for value in List:
        _type,SeroFunc = ser_switch(value)
        retV=f'{retV}{SeroFunc(_type,value)} '
    retV=f'{retV}ᐺᐶ'
    return retV

def seroTuples(retV,tupel):
    retV=f'ᐻ{retV}'
    for value in tupel:
        _type,SeroFunc = ser_switch(value)
        retV=f'{retV}{SeroFunc(_type,value)} '
    retV=f'{retV}ᐼᐶ'
    return retV


def ser_switch(obj):
    switcher = {
        type(None) : ("ᐰ",NoneSerilazation),
        bool       : ("ᐱ",simpleSerilazation),
        int        : ("ᐲ",simpleSerilazation),
        float      : ("ᐳ",simpleSerilazation),
        str        : ("ᐴ",strSerilazation),
        list       : ("",seroList),
        tuple      : ("",seroTuples),
        dict       : ("",seroDict)
    }
    return switcher.get(type(obj), ("",seroObjects))


def dumps(obj):
    _type,SeroFunc = ser_switch(obj)
    SeroFunc(_type,obj)
    return SeroFunc(_type,obj)


if __name__ == '__main__':


    import pickle
    import time


    integer=12
    Float=12.1
    listValues=[1,2,42,1]
    tupleNum=(1,4,6,[1,4,5])
    othamn = person("otham","white",23,'fuck')
    mac=shope(othamn,'squrre',69,"jeddah")
    jeddah = twon('jeddah',othamn,mac,'jeddah','soemthidskahfnlsadj')
    dictory={
        1:listValues,
        2:tupleNum,
        3:jeddah

    }
    t0=time.time()

    for _ in range(100000):
        dumps(None)
        dumps(integer)
        dumps(Float)
        dumps(listValues)
        byteStream=dumps(tupleNum)

    print(time.time()-t0)
    t0=time.time()

    for _ in range(100000):
        pickle.dumps(None)
        pickle.dumps(integer)
        pickle.dumps(Float)
        pickle.dumps(listValues)
        pickle.dumps(tupleNum)

    print(time.time()-t0)





