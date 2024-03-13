#!/usr/bin/env python3

#sever stuff
from socket import *
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1) # at least 1 queued connections
print('the sever is ready to receive')
while 1:
    connectionSocket, addr = serverSocket.accept() #connectionSocket is name of connected client
    sentence = connectionSocket.recv(1024)
    capitalizedSentence = sentence.upper()
    connectionSocket.send(capitalizedSentence)
    connectionSocket.close()

