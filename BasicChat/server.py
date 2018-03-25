#!/usr/bin/python3

import threading
import socket
import sys
import struct
from util import Util

def handleUsers(client):
    global userCount, clientList

    ID = addingClient(client, True)

    while True:
        data = client.recv(BUFSIZE).strip()
        if not data:
            break
        data = data.decode("utf-8")
        print(ID, data)
        broadCast(ID, data)

    addingClient(client, False)

def addingClient(client, flag):
    global lock, userCount, clientList

    ID = ""
    lock.acquire()
    if flag is True:
        ID = verifyID(client)
        broadCast(ID, "has been joined!!!")
    else:
        if client in clientList:
            userCount -= 1
            broadCast(clientList[client], "has been leaved!!!")
            del clientList[client]

    print("Member Count %d" % len(clientList))
    lock.release()

    return ID

def verifyID(client):
    global clientList, userCount

    while True:
        ID = client.recv(BUFSIZE).strip()
        ID = ID.decode("utf-8")

        if ID not in clientList.values():
            break

        client.send(struct.pack("i", -1))

    client.send(struct.pack("i", 0))
    userCount += 1
    clientList[client] = ID

    return ID

def broadCast(ID, string):
    global clientList
    data = "[" + ID + "] " + string
    data = data.encode("utf-8")

    for client in clientList.keys():
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

            for c in clientList.keys():
                c.close()
        break

    if client is not None:
        t = threading.Thread(target=handleUsers, args=(client,))
        t.daemon = True
        t.start()

server.close()
print("Server End")
