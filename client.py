#client stuuf
from socket import *
serverName = '172.27.107.120'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM) #ipv4, tcp socket
clientSocket.connect((serverName, serverPort))
sentence = input('input lowercase sentence:')
clientSocket.send(sentence.encode())
modifiedSentence = clientSocket.recv(1024)
print('From Sever:', modifiedSentence.decode())
clientSocket.close()