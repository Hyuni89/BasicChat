#!/usr/bin/python3

import threading
import socket
import sys
from util import Util

def handleUsers(client):
    global userCount, clientList

    ID = client.recv(BUFSIZE).strip()
    ID = ID.decode("utf-8")
    addingClient(ID, client, True)
    broadCast(ID, "has been joined!!!")

    while True:
        data = client.recv(BUFSIZE).strip()
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

util = Util()

if len(sys.argv) > 1:
    if util.parseOptions(sys.argv) != 0:
        sys.exit(0)

HOST = util.ADDR
PORT = util.PORT
ADDR = (HOST, PORT)
BUFSIZE = util.BUFSIZE
lock = threading.Lock()
userCount = 0
clientList = dict()

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
