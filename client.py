import socket
import os #for operating system
import subprocess  #for processes that are on a windows laptop

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "172.27.107.120" #ip address of server
port = 12001

socket.connect((host, port)) #to establish connection

while True:
    data = socket.recv(1024)
    if data.decode() == 'do you want data?':
        print('From server!! --> ', data.decode(), '\n')
        reply = input('yes or no? --> ')
        socket.send(reply.encode())
    elif data.decode() == '0 attempts remaining':
        null = ' '
        socket.send(null.encode())
    else:
        #while data_two != 'better luck next time':
        print('From server!! --> ', data.decode(), '\n')
        reply = input('answer: ')
        socket.send(reply.encode())
