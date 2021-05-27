import sys
class output():
    def __init__(self,net):
        self.stdout=sys.stdout
        self.net = net
        self.num=0

    def write(self, text):
        self.num+=1
        if self.num%2:
            self.net.sendOutput(text)

    def flush(self):
        self.stdout.flush()


class error():
    def __init__(self,net):
        self.stderr = sys.stderr
        self.net = net

    def write(self, text):
        self.net.sendError(str(text))

    def flush(self):
        self.stderr.flush()


