#!/usr/bin/python3

import socket
import sys
import threading
import struct
from util import Util

def listen(client):
    while True:
        data = client.recv(BUFSIZE).strip()
        print(data.decode("utf-8"))

        if not data:
            break

def verifyID(client):
    while True:
        print("Your ID : ", end="")
        ID = input()

        if len(ID) > 0xFF:
            ID = ID[:0xFF]

        client.send(ID.encode("utf-8"))
        data = client.recv(BUFSIZE)

        if struct.unpack("i", data[:4])[0] == 0:
            break

        print("ID already exist. Try again")

util = Util()

if len(sys.argv) > 1:
    if util.parseOptions(sys.argv) != 0:
        sys.exit(0)

HOST = util.ADDR
PORT = util.PORT
ADDR = (HOST, PORT)
BUFSIZE = util.BUFSIZE

client = socket.socket()
res = client.connect(ADDR)

verifyID(client)
print("Connected!")

t = threading.Thread(target=listen, args=(client,))
t.daemon = True
t.start()

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
