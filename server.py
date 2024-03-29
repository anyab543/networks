import socket
import threading

class handle_client(threading.Thread): #when called thread is made each time (aka thread made for each client)
    def __init__(self, client, address, connections):
        super().__init__() #initialising parameters
        self.client = client
        self.address = address
        self.connections = connections
        self.lives = 3

    def run(self): #function from threading library
        self.begin()

    def begin(self): #sends riddle to each client when they connect
        try:
            welcome_msg = 'you must solve this riddle in 3 attempts! "What question can you never answer yes to?" \n'
            self.client.send(str.encode(welcome_msg))
            print("Riddle sent\n")
            answer = 'are you asleep yet?'
            self.riddle(answer) #passing answer parameter
        
        finally: #ensures connection will close when riddle function done (may need to remove this depending on service)
            self.client.close()

                


    def riddle(self, answer):
        try:
            while self.lives >= 1:
                response = self.client.recv(1024)
                if response.decode() == answer:
                    self.success() 
                    return #exit while loop and therefore function
                else:
                    self.lives = self.lives - 1 #increment lives
                    if self.lives == 0:
                        self.fail() #fail message
                    else:
                        attempts = str(self.lives) + ' attempts remaining\n'
                        self.client.send(str.encode(attempts))

        except Exception as e:
            print("Error with sending riddle message: \n", e)

    def success(self):
        try:
            completed = 'Congrats you solved the riddle! Do you want some information?\n' #or service, tailor message to suit here (message must go here tho)
            self.client.send(str.encode(completed))
            response = self.client.recv(1024)
            if response.decode() == 'yes':
                self.service() #got to servive function
            else:
                self.end_conn() #conection closes otherwise
        except:
            print("Error with success message")

    def fail(self):
        try:
            fail = 'Failed security test. Press any key to exit programm\n'
            self.client.send(str.encode(fail))
            print("Client failed riddle test")
            with mutex: # critical section
                self.connections.remove(self.address)  #removes address from the list
            self.client.close() #close connection
        except:
            print("Error with fail message")

    def service(self):
        #add service stuuf here
        print(" blah blah blah")

    def end_conn(self):
        try:
            msg = 'Program is closing, press any key to exit programm\n'
            self.client.send(str.encode(msg))
            print("Sending closing message\n")

            with mutex: #critical section
                self.connections.remove(self.address) #removes address from the list
            self.client.close()
        except:
            print("Error with closing message")
        
def main():
    global mutex #initialise mutex
    mutex = threading.Lock()
    
    global all_connections #initialise list
    all_connections = []

    host = ""
    port = 1113

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #ipv4 and tcp connection
    server.bind((host, port))
    server.listen() #listen for connections

    print("Server listening\n")

    while True:
        client, address = server.accept() #accept connection
        print("Connection from: ", str(address))
        with mutex: #critical section
            all_connections.append(address) #add address to the list
        
        
        c_handler = handle_client(client, address, all_connections) #calling function
        c_handler.start() #start function

if __name__ == "__main__":
    main() #the main
