#!/usr/bin/python2

import socket
import random
import math
import sys

HOST = "localhost"
PORT = 1111
ADDR = (HOST, PORT)

server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
value = server.getsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST)
server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, value)
server.bind(ADDR)
server.listen(5)
client, address = server.accept()
print address

for i in range(100):
    correct = False
    N = random.randrange(1, 1000)
    C = int(math.log(N, 2)) + 1
    number = random.randrange(0, N)
    sendString = "N=" + str(N) + " C=" + str(C)
    print sendString
    client.send(sendString + "\n")

    for j in range(C):
        try:
            data = map(int, client.recv(2048).strip().split())
        except ValueError as e:
            client.send("Data format error\n")
            server.close()
            sys.exit(1)
        
        if number in data:
            client.send(str(len(data) * 10 - 1) + "\n")
        else:
            client.send(str(len(data) * 10) + "\n")
    
    try:
        data = client.recv(1024).strip()
        print data
        data = int(data)
    except ValueError as e:
        client.send("Answer format error\n")
        server.close()
        sys.exit(1)
    if data == number:
        client.send("Correct(" + str(i) + ")\n")
    else:
        client.send("Wrong\n")
        server.close()
        sys.exit(1)

client.send("You got it!!\n")
server.close()
client.close()
