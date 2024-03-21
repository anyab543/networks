import socket
import sys #implement command lines and terminal commmands

#making socket here
def make_socket():
    try:
        global host
        global port
        global socket
    
        host = ''
        port = 1200
        socket = socket.socket() #socket made here

    except socket.error as message:
        print("Error with making socket" + str(message))

#binding port and ip here
def binding_socket():
    try:
        global host
        global port
        global socket

        print("Binding port: " + str(port))
        socket.bind((host,port)) #bining the ip and port num here in the socket
        socket.listen(4) #listening for 4 connections max (get error if try and do more)

    except socket.error as message:
        print("Error with binding socket " +str(message) + '\n' + "Retry: ") #if there is an error message will print adn will try and bind again
        binding_socket()

#accepting connection(s)
def accepting_connection():
    connection, address = socket.accept() #ip address and port stored in address  (a list) variable
    print("Connection found: " + "ip address is = " + str(address[0] + " port num is = " + str(address[1])))
    send_message(connection)
    connection.close() #closing connection

#sending messages to client
def send_message(connection):
    while True:
        command = input()
        if command == 'bye':
            connection.close() #connection is closed
            socket.close() #socket is close
            sys.exit() #command prompt is closed
        if len(str.encode(command)) > 0: #give length of string
            connection.send(str.encode(command))
            response = str(connection.recv(1024), "utf-8") #converting response from bytes to string 
            print(response, end='') #goes onto new line after printing the response

def main():
    make_socket()
    binding_socket()
    accepting_connection()

main()
