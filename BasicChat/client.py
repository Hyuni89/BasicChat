#!/usr/bin/python3

import socket
import sys

HOST = "localhost"
PORT = 8888
ADDR = (HOST, PORT)

if len(sys.argv) > 1:
    print("proc arg")
    pass

client = socket.socket()
res = client.connect(ADDR)
print(res)

while True:
    try:
        data = sys.stdin.readline()
        res = client.send(data.encode("utf-8"))
        print(res)
    except KeyboardInterrupt:
        break

client.close()
print("Disconnect")
