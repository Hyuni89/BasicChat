#!/usr/bin/python3

import threading
import socket
import sys

def handleUsers(client):
    global userCount, clientList

    ID = client.recv(1024).strip()
    ID = ID.decode("utf-8")
    addingClient(ID, client, True)
    broadCast(ID, "has been joined!!!")

    while True:
        data = client.recv(1024).strip()
        if not data:
            break
        data = data.decode("utf-8")
        print(ID, data)
        broadCast(ID, data)

    addingClient(ID, client, False)
    broadCast(ID, "has been leaved!!!")

def addingClient(ID, client, flag):
    global lock, userCount, clientList

    lock.acquire()
    if flag is True:
        if ID not in clientList:
            userCount += 1
            clientList[ID] = client
    else:
        if ID in clientList:
            userCount -= 1
            del clientList[ID]
    lock.release()

def broadCast(ID, string):
    global clientList
    data = "[" + ID + "] " + string
    data = data.encode("utf-8")

    for client in clientList.values():
        res = client.send(data)

HOST = "localhost"
PORT = 8888
ADDR = (HOST, PORT)
lock = threading.Lock()
userCount = 0
clientList = dict()

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
        if len(clientList) > 0:
            msg = "Server Closed... Sorry!"
            broadCast("", msg.encode("utf-8"))

            for c in clientList.values():
                c.close()
        break

    if client is not None:
        t = threading.Thread(target=handleUsers, args=(client,))
        t.daemon = True
        t.start()

server.close()
print("Server End")
