#!/usr/bin/python2

import socket

def genNum(left, right):
    if left == right:
        return str(left)
    ret = ""
    for i in range(left, right):
        ret += str(i) + " "
    print ret[:-1]
    return ret[:-1]

HOST = "localhost"
PORT = 1111
ADDR = (HOST, PORT)

client = socket.socket()
client.connect(ADDR)

for i in range(100):
    data = client.recv(1024).strip().split()
    N = int(data[0][2:])
    C = int(data[1][2:])
    print N, C

    left = 0
    right = N
    for j in range(C):
        mid = (left + right) / 2
        compare = (mid - left) * 10
        client.send(genNum(left, mid) + "\n")

        data = int(client.recv(1024).strip())
        print "return:", data
        if data == 9:
            continue

        if data == compare:
            left = mid
        else:
            right = mid
    
    client.send(genNum(left, (left + right) / 2) + "\n")
    data = client.recv(1024)
    print data

flag = client.recv(1024)
print flag
client.close()
