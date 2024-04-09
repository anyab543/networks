#library needed
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #tcp connection with ipv4
host = "172.27.107.120" #ip address of server
port = 9999 #port used for connection

#only works when serevr and client on same device
#host_name = socket.gethostname() #getting the local host name
#host = socket.gethostbyname(host_name) #getting the ip addresss  of local host

c_socket = (host, port)
client.connect(c_socket) #to establish connection

while True:
    data = client.recv(1024) #receiving data
    print('Server>  ', data.decode(), '\n') #print data that is decoded
    if 'any key to exit programm' in data.decode(): #if 'any key to exit program' in any part of recieved message
        client.close() #close connection
    elif 'order placed for' in data.decode(): #close connection when an order has been placed
        client.close()
    else:
        reply = input('Reply>  ') #user input reply
        client.send(reply.encode()) #send the reply that is encoded to server
