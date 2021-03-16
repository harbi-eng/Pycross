#!/usr/bin/env python
# Author: Saud Wasly
# copyrgiht: Saud Wasly
class RemoteObject(object):
  pass

X = RemoteObject()
print(X is RemoteObject)

def serialize( obj):
  # print(X is RemoteObject)
  retV = ''
  if obj is None:
    retV = 'None'
  elif type(obj) is bool:
    retV = 'bool@%s' % int(obj)
  elif type(obj) is int:
    retV = 'int@%s' % obj
  elif type(obj) is float:
    retV = 'float@%s' % obj
  elif type(obj) is str:
    retV = 'str@%s' % obj

  # elif type(obj) is RPC_pkt:
  #   s = delimter.join(['RPC', obj.initiator, str(obj.ID), obj.RequestType, obj.body])
  #   # s = 'RPC'+ delimter +  '%d,%s,%s'%(obj.ID, obj.RequestType, obj.body)
  #   retV = s

  elif type(obj) is list:
    s = ''
    s = '%s^'.join(serialize(i) for i in obj)
    # for i in obj:
    #   s += '%s^' % serialize(i)
    # s = s.replace('@', ':')
    if len(s) > 0:
      retV = 'list@' + s[:-1]

  elif type(obj) is tuple:
    s = ''
    for i in obj:
      s += '%s^' % serialize(i)
    s = s.replace('@', ':')
    if len(s) > 0:
      retV = 'tuple@' + s[:-1]

  elif type(obj) is dict:
    s = ''
    for key in obj:
      s_key = serialize(key)
      s_obj = serialize(obj[key])
      s += '%s->%s^' % (s_key, s_obj)
    s = s.replace('@', ':')
    if len(s) > 0:
      retV = 'dict@' + s[:-1]

  elif type(obj) is RemoteObject:
    Robj = obj  # type:RemoteObject
    retV = 'RemoteObject@%s;%s;%s' % (Robj.Title, Robj.ObjName, Robj.Creator)
  elif type(obj) is RemoteFunction:
    # Rfunc = obj #type:RemoteFunction
    # FuncName = Rfunc.FuncName
    retV = 'RemoteFunction@%s;%s;%s' % (obj.Title, obj.FuncName, obj.Creator)
    # retV = 'RemoteFunction@%s'%FuncName
  elif type(obj) is RemoteException:
    RExecpt = obj  # type:RemoteException
    retV = 'RemoteException@%d;%s' % (RExecpt.Number, RExecpt.msg)

  # elif type(obj) == types.MethodType or type(obj) == types.FunctionType:
  #   obj_id = 'DynamicObj' + hex(id(obj))
  #   rObj = RemoteObject(str(obj), obj_id, Name,
  #   _Dynamic_Objects[obj_id] = (rObj, obj)
  #   retV = serialize(rObj)

  else:  # Other complex Object including functions
    pass
    obj_id = 'DynamicObj' + hex(id(obj))
    title = str(obj).replace(',', ' ')
    # rObj = RemoteObject(title, obj_id, Name,
    # _Dynamic_Objects[obj_id] = (rObj, obj)
    # retV = serialize(rObj)

  return retV


def deserialize( cmd):
    retV = ''
    if cmd.startswith('RPC'+ delimter):
      retV = RPC_pkt()
      cmdL = cmd.split(delimter)
      retV.initiator = cmdL[1]
      retV.ID = int(cmdL[2])
      retV.RequestType = cmdL[3]
      body = cmdL[4:] #type:str
      retV.body = body[0].split(',')
      pass
    else:
      cmdL = cmd.split('@')
      sType = cmdL[0]

      #FIXME: Add List and Dict treatment
      if sType == 'None':
        val = None
        retV = val
      elif sType == 'int':
        val = cmdL[1]
        retV = int(val)
      elif sType == 'bool':
        val = cmdL[1]
        retV = bool(int(val))
      elif sType == 'float':
        val = cmdL[1]
        retV = float(val)
      elif sType == 'str':
        val = cmdL[1]
        retV = val
      elif sType == 'str':
        val = cmdL[1]
        retV = val


      elif sType == 'list':
        val = cmdL[1]
        val = val.replace(':', '@')
        valL = val.split('^')
        for i in range(len(valL)):
          valL[i] = deserialize(valL[i])
        retV = valL
      elif sType == 'tuple':
        val = cmdL[1]
        val = val.replace(':', '@')
        valL = val.split('^')
        for i in range(len(valL)):
          valL[i] = deserialize(valL[i])
        retV = tuple(valL)
      elif sType == 'dict':
        val = cmdL[1]
        val = val.replace(':', '@')
        dict_L = [] if val == '' else val.split('^')
        retV_D = {}
        for i in range(len(dict_L)):
          s_key, s_val = dict_L[i].split('->')
          key = deserialize(s_key)
          val = deserialize(s_val)
          retV_D[key] = val
        retV = retV_D
      elif sType == 'RemoteObject':
        Title, FullName, Creator = cmdL[1].split(';')
        retV = RemoteObject(Title, FullName, Creator)
      elif sType == 'RemoteFunction':
        FuncName = cmdL[1]
        Title, FullName, Creator = cmdL[1].split(';')
        retV = RemoteFunction(Title, FullName, Creator)
      elif sType == 'RemoteException':
        number, msg = cmdL[1].split(';')
        retV = RemoteException(number, msg)

    return retV


if __name__ == '__main__':
    L = [1,2,3,'dfds1', [5,6,7,'saud2']]
    s = serialize(L)
    print(s)