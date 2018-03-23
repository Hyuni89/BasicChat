#!/usr/bin/python3

import socket
import sys
import threading
from util import Util

def listen(client):
    while True:
        data = client.recv(BUFSIZE).strip()
        print(data.decode("utf-8"))

        if not data:
            break

util = Util()

if len(sys.argv) > 1:
    if util.parseOptions(sys.argv) != 0:
        sys.exit(0)

HOST = util.ADDR
PORT = util.PORT
ADDR = (HOST, PORT)
BUFSIZE = util.BUFSIZE

print("Your ID : ", end="")
ID = input()
if len(ID) > 0xFF:
    ID = ID[:0xFF]

client = socket.socket()
res = client.connect(ADDR)

t = threading.Thread(target=listen, args=(client,))
t.daemon = True
t.start()

client.send(ID.encode("utf-8"))

while True:
    try:
        data = sys.stdin.readline()
        data = data.encode("utf-8")
        if len(data) > BUFSIZE:
            data = data[:BUFSIZE]
        res = client.send(data)
    except KeyboardInterrupt:
        break

client.close()
print("Disconnect")
