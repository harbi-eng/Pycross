import sys

class output():
    def __init__(self,net):
        self.stdout=sys.stdout
        self.net = net

    def write(self, text):
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


