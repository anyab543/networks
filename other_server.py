import socket
import sys #implement command lines and terminal commmands
import threading
import time
from queue import Queue

NUM_THREAD = 2
NUM_OF_JOBS = [1, 2] #job one is to listen and accept and job 2 is to send messages and handle connections with existing clients
queue = Queue()
total_connections = []
total_addresses = []

#thread 1 here that can listen and accept connections
#making socket here
def make_socket():
    try:
        global host
        global port
        global server
    
        host = "172.27.107.120"
        port = 12000
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket made here

    except socket.error as message:
        print("Error with making socket" + str(message))

#binding port and ip here
def binding_socket():
    try:
        global host
        global port
        global server

        print("Binding port: " + str(port))
        server.bind((host,port)) #bining the ip and port num here in the socket
        server.listen(4) #listening for 4 connections max (get error if try and do more)

    except socket.error as message:
        print("Error with binding socket " +str(message) + '\n' + "Retry: ") #if there is an error message will print adn will try and bind again
        binding_socket()

#saving clients to list that have connected
def get_connections():
    for i in total_connections:
        i.close() #going through each connection and closing it

    del total_connections[:] #deleting all connection in the list
    del total_addresses[:] #deleting all addresses in the list

    while True:
        try:
            connection, address = server.accept()
            server.setblocking(1) #prevents time out (1 for true)

            total_connections.append(connection) #adding connection to the list
            total_addresses.append(address) #adding address to the list
            print("Connection! : " + address[0])
            welcome_msg = 'you must solve this riddle in 3 attempts! "What question can you never answer yes to?" \n'
            connection.send(str.encode(welcome_msg))
            threading.Thread(target=messages, args=(connection,)).start()

        except:
            print("Error with connecting")

#thread 2 here that can see, select and send messsages to clients
def start_terminal():
 #send message to all clients
            for index, connection in enumerate(total_connections):
                print("connected to this client: " + str(total_addresses[index][0]))
                print(str(total_addresses[index][0]) + ">", end="")
                messages(connection)



#prints out clients we are connected to
list = ''
def connection_list():
    list = '\n'.join([str(connection.getpeername()) for connection in total_connections])
    print(f"list: {list}")


#choosing specific client and returns the value of the client (aka its number)
def get_client(command):
    try:
        client_num = command.replace('select ', '') #replaceing select that is in commadn with a blank
        client_num = int(client_num) #converting it into a number
        connection = total_connections[client_num] #get object of connections
        
        print("connected to this client: " + str(total_addresses[client_num][0]))
        print(str(total_addresses[client_num][0]) + ">", end="") #formating to look like new terminal just for specific client (123.456.789.0> )

        return connection

    except:
        print("connection doesn't exist")
        return None
    
#sending messages to client
def messages(connection):
    try:
        lives = 3
        answer = 'are you asleep yet?'

        while lives > 0:
            response = connection.recv(1024)

            if response.decode() == answer:
                completed = 'congrats you solved the riddle!\n'
                connection.send(str.encode(completed))
                break

            else:
                lives = lives -1
                attempts = str(lives) + ' attempts remaining\n'
                connection.send(str.encode(attempts))

                if lives == 0:
                    fail = 'better luck next time'
                    connection.send(str.encode(fail))
                    client_num = total_connections.index(connection)
                    print('client ' + str(client_num) + ' failed to solve riddle, going back to terminal\n')
                    break

    except:
        print("error with sending message :/ ")
                
#making thread
def make_thread():
    for _ in range(NUM_THREAD): #for loop in the range of num of threads (aka 2)
        thread = threading.Thread(target=action) #creating thread
        thread.daemon = True #thread will end when program ends
        thread.start() #starting thread

#does next action in the queue
def action():
    while True:
        x = queue.get()

        if x == 1: #thread 1
            make_socket()
            binding_socket()
            get_connections()

        if x == 2: #thread 2
            start_terminal()
        
        queue.task_done()

def make_action():
    for x in NUM_OF_JOBS:
        queue.put(x) #putting number of jobs list into queue formate cause threads work woth queues

    queue.join()


make_thread()
make_action()