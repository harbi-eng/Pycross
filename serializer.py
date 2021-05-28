"""
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

# coding=utf-8
replacment = ['None', 'bool', 'int', 'float', 'str', '\"', '_object', ',', '{', '}', '[', ']', '(', ')', ':']
signs = ['ᐰ', 'ᐱ', 'ᐲ', 'ᐳ', 'ᐴ', 'ᐿ', 'ᐵ', 'ᐶ', 'ᐷ', 'ᐸ', 'ᐹ', 'ᐺ', 'ᐻ', 'ᐼ', 'ᐽ']
import sys

def loads(data):
    global signs, replacment
    try:
        if "jython" in sys.executable:
            raise Exception()

        data = data.decode()


        for s, r in zip(signs, replacment):

            if s in data:
                data = data.replace(s, r)
                
        return eval(data[:-1])
    except:
        # data = u' '.join(data).encode('utf-8').strip()
        data = data.decode('utf-8')

        for s, r in zip(signs,replacment):
            s=s.decode('utf-8')
            if s in data:
                data = data.replace(s, r)

        return eval(data[:-1])




def _object(dict):
    global classesDict
    _type = dict['className']
    if _type not in classesDict.keys():
        classesDict[_type] = type("slave_%s"%_type, (globals()[_type],), {"__init__": func})
    ob = classesDict[_type]()
    ob.__dict__ = dict.copy()

    return ob


classesDict = {}


def func(self):
    pass


def simpleSerilazation(_type, obj):
    return "%sᐻ%sᐼᐶ"%(_type,obj)


def NoneSerilazation(_type, obj):
    return "%sᐶ"%obj


def strSerilazation(_type, obj):
    return "ᐴᐻᐿᐿᐿ%sᐿᐿᐿᐼᐶ"%obj


def seroObjects(retV, obj):
    retV = 'ᐵᐻᐷ ᐴᐻᐿclassNameᐿᐼᐽᐴᐻᐿ%sᐿᐼᐶ %s'%(obj.__class__.__name__,retV)
    for key, value in obj.__dict__.items():
        Vtype, VSeroFunc = ser_switch(value)
        Ktype, KSeroFunc = ser_switch(key)
        retV = '%s%sᐽ%s '%(retV,KSeroFunc(Ktype, key)[:-1],VSeroFunc(Vtype, value))
    retV = '%sᐸᐼᐶ'%retV
    return retV


def seroDict(retV, dict):
    retV = 'ᐷ%s'%retV
    for key, value in dict.items():
        Vtype, VSeroFunc = ser_switch(value)
        Ktype, KSeroFunc = ser_switch(key)

        retV = '%s%sᐽ%s '%(retV,KSeroFunc(Ktype, key)[:-1],VSeroFunc(Vtype, value))
    retV = '%sᐸᐶ'%retV
    return retV


def seroList(retV, List):
    retV = 'ᐹ%s'%retV
    for value in List:
        _type, SeroFunc = ser_switch(value)
        retV = '%s%s '%(retV,SeroFunc(_type,value))
    retV = '%sᐺᐶ'%retV
    return retV


def seroTuples(retV, tupel):
    retV = 'ᐻ%s'%retV
    for value in tupel:
        _type, SeroFunc = ser_switch(value)
        retV = '%s%s '%(retV,SeroFunc(_type,value))
    retV = '%sᐼᐶ'%retV
    return retV


def ser_switch(obj):
    switcher = {
        type(None): ("ᐰ", NoneSerilazation),
        bool: ("ᐱ", simpleSerilazation),
        int: ("ᐲ", simpleSerilazation),
        float: ("ᐳ", simpleSerilazation),
        str: ("ᐴ", strSerilazation),
        list: ("", seroList),
        tuple: ("", seroTuples),
        dict: ("", seroDict),
        object:("", seroObjects)
    }
    return switcher.get(type(obj), )


def dumps(obj):
    _type, SeroFunc = ser_switch(obj)
    result=SeroFunc(_type, obj)
    # print(result.encode('utf-8'))
    try:
        if "jython" in sys.executable:
            raise Exception()
        return result.encode('utf-8')
    except Exception:
        return unicode(result,'utf-8').encode('utf-8')

