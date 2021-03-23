import re
from importlib import import_module

def filesetup(keywords,code):
    match = re.search('[\s\S]*import\s*pycross', code)
    objects=[]

    buffer = code.replace(match.group(), '').split('\n')

    lines = [[line for line in buffer if key in line] for key in keywords]
    for line_per_key in lines:
        for line in line_per_key:
            obj_name = line.split(".")[0].replace(" ", "")
            if obj_name not in objects:
                objects.append("@" + obj_name)
                objects.append(obj_name)

    buf = []
    for line in buffer:
        for index, obj in enumerate(objects):
            if obj in line:
                break
            if index == len(objects) - 1:
                buf.append(line)

    buf = "\n".join(buf)
    file = open('MainFile.py', "+w")
    file.write(buf)
    file.close()

    return buf