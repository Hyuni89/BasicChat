#!/usr/bin/python3

import socket
import sys
import threading

def listen(client):
    while True:
        data = client.recv(1024).strip()
        print(data.decode("utf-8"))

        if not data:
            break

HOST = "localhost"
PORT = 8888
ADDR = (HOST, PORT)

if len(sys.argv) > 1:
    print("proc arg")
    pass

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
        res = client.send(data)
    except KeyboardInterrupt:
        break

client.close()
print("Disconnect")
