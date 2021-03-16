import sys

class stdout2():
    def __init__(self):
        self.stdout=sys.stdout

    def write(self, text):
        self.stdout.write("fuck yourself")

    def flush(self):
        self.stdout.flush()


class stderr2():
    def __init__(self):
        self.stderr = sys.stderr

    def write(self, text):
        self.stderr.write(text)
        pass

    def flush(self):
        self.stderr.flush()


sys.stdout = stdout2()



