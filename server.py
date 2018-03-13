#!/usr/bin/python3

import threading
import socket
import sys

HOST = "localhost"
PORT = 8888
ADDR = (HOST, PORT)

if len(sys.argv) > 1:
    print("proc arg")
    pass

server = socket.socket()
server.bind(ADDR)
server.listen()
client, address = server.accept()
print(client, address)
data = client.recv(1024)
print(data)
server.close()
