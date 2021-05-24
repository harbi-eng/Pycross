
def filesetup(keywords,code):
    objects=[]

    buffer = code.split('\n')

    lines = [[line for line in buffer if key in line] for key in keywords]
    for line_per_key in lines:
        for line in line_per_key:
            obj_name = line.split(".")[0].replace(" ", "")
            if obj_name not in objects:
                if '=' in obj_name:
                    obj_name=obj_name.split('=')[0]
                objects.append("@" + obj_name)
                objects.append(obj_name)
    count=2
    buf = []
    for line in buffer:
            for index, obj in enumerate(objects):
                if obj in line:
                    if count>0:
                        count=count-1
                    elif 'createremoteobject' not in line:
                        break
            else: buf.append(line)

    buf = "\n".join(buf)
    file = open('MainFile.py', "+w")
    file.write(buf)
    file.close()

    return buf
