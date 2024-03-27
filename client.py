import socket
import os #for operating system
import subprocess  #for processes that are on a windows laptop

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "172.20.10.2" #ip address of server
port = 12000

client.connect((host, port)) #to establish connection

while True:
    data = client.recv(1024)
    if data.decode() == 'bye':
        client.close()
        break
    else:
        print('From server!! --> ', data.decode(), '\n')
        reply = input('answer: ')
        socket.send(reply.encode())
