#!/usr/bin/python3

import threading
import socket
import sys

def handleUsers(client):
    while True:
        data = client.recv(1024).decode("utf-8").strip()
        if not data:
            break
        print(data)
    

HOST = "localhost"
PORT = 8888
ADDR = (HOST, PORT)

if len(sys.argv) > 1:
    print("proc arg")
    pass

server = socket.socket()
server.bind(ADDR)
server.listen()

while True:
    try:
        client, address = server.accept()
        print(client, address)
    except KeyboardInterrupt:
        break

    if client is not None:
        t = threading.Thread(target=handleUsers, args=(client,))
        t.start()

server.close()
print("Server End")
