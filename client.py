#!/usr/bin/python3

import socket
import sys

HOST = "localhost"
PORT = 8888
ADDR = (HOST, PORT)

client = socket.socket()
res = client.connect(ADDR)
print(res)

data = sys.stdin.readline()
res = client.send(data.encode("utf-8"))
print(res)
client.close()
