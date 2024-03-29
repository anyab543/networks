import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "172.27.107.120" #ip address of server
port = 1113

client.connect((host, port)) #to establish connection

while True:
    data = client.recv(1024)
    print('Server>  ', data.decode(), '\n')
    if 'any key to exit programm' in data.decode(): #if that in any part of recieved message
        input('Reply>  ')
        client.close()
    else:
        reply = input('Reply>  ')
        client.send(reply.encode())
