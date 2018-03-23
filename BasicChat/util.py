import re

class Util:
    def __init__(self):
        self.ADDR = "localhost"
        self.PORT = 8888
        self.BUFSIZE = 1024

    def setAddress(self, address):
        self.ADDR = address

    def setPort(self, port):
        self.PORT = port

    def setBufferSize(self, bufsize):
        self.BUFSIZE = bufsize

    def parseOptions(self, args):
        for i in range(1, len(args), 2):
            if args[i] == "--port":
                try:
                    self.PORT = int(args[i + 1])
                except:
                    return self.help()
            elif args[i] == "--address":
                if bool(re.match("[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", args[i + 1])) is True:
                    self.ADDR = args[i + 1]
                else:
                    return self.help()
            else:
                return self.help()

        return 0

    def help(self):
        print("Usage: ./exec <options>")
        print("\t--port <num>\t\tsetting port(default 8888)")
        print("\t--address <IP address>\tsetting address(default localhost)")

        return -1
