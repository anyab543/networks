# libraries needed
import socket
import threading
import time
import random

#array of riddle questions
riddles = ["The more of this there is, the less you see. What is it?",
           "Which fish costs the most?",
           "What goes up, but never comes down?",
           "What must be broken before you can use it?",
           "What is full of holes but still holds water?",
           "I am easy to lift, but hard to throw. What am I?"]
#array of riddle answers
riddle_answers = ["darkness",
                  "goldfish",
                  "age",
                  "egg",
                  "sponge",
                  "feather"]


class handle_client(threading.Thread): #when called thread is made each time (aka thread made for each client)
    def __init__(self, client, address, connections):
        super().__init__() #initialising parameters
        self.client = client
        self.address = address
        self.connections = connections
        self.lives = 3

    def run(self): #function from threading library
        self.begin()

    #sends riddle to each client when they connect
    def begin(self): 
        try:
            random_index = random.randint(0, len(riddles) - 1) #getting random index from riddles array
            self.client.send(f"Welcome! Solve this riddle: {riddles[random_index]}\n.".encode()) #inital message to clitn with random riddle
            print(f"Riddle sent to {self.address}\n") #display to server that riddle was sent
            answer = riddle_answers[random_index] #answer key needed for the riddle
            self.riddle(answer) #passing answer parameter
        
        finally: #ensures connection will close when riddle function done
            self.client.close()

    #actions taken when the riddle is or isn't solved
    def riddle(self, answer):
        try:
            while self.lives >= 1:
                response = self.client.recv(1024) #recieve message from client
                if response.decode() == answer: #if the aswner to the riddle go to success function
                    self.success() 
                    return #exit while loop and therefore function
                else:
                    self.lives = self.lives - 1 #increment lives
                    if self.lives == 0: #if no live go to fail function
                        self.fail()
                    else:
                        attempts = str(self.lives) + ' attempts remaining\n' #send to client how many lives they have left
                        self.client.send(str.encode(attempts))

        except Exception as e: #prints if an error has occured in this function
            print("Error with sending riddle message: \n", e)

    #start of service implementation when riddle is solved
    def success(self):
        try:
            global all_votes, che_votes, pep_votes
            completed = 'Congrats you solved the riddle! cheese or pepperoni?\n' #client recieves message only when riddle is solved
            self.client.send(str.encode(completed))
            response = self.client.recv(1024) #client response so should be cheese or pepperoni

            with mutex: #critical region so lock
                all_votes = all_votes + 1 #increment all votes counter
            
            if response.decode() == 'cheese': #if repsonse cheese
                with mutex: #critical region so lock
                    che_votes = che_votes + 1 #increment cheese counter

                self.voting() #go to voting function

            elif response.decode() == 'pepperoni': #if response pepperoni
                with mutex: #critical region so lock

                    pep_votes = pep_votes + 1 #increment pepperoni counter
                self.voting() #go to voting function

            else:
                self.end_conn() #conection closes otherwise

        except:
            print("Error with success message") #prints if error occurs

    #fail function when riddle is not solved
    def fail(self):
        try:
            print(f"Client, {self.address}, failed riddle test") #prints to let server know that client failed
            fail = 'Failed security test. Press any key to exit programm\n' #fail message sent to client
            self.client.send(str.encode(fail))

            with mutex: # critical region so lock
                self.connections.remove(self.address)  #removes address from the list

            self.client.close() #close connection
        except:
            print("Error with fail message") #prints if error occurs

    def voting(self):
        try:
            global all_votes, che_votes, pep_votes, all_connections
            while all_votes != len(all_connections):
                time.sleep(1) #thread goes to sleep until all votes have been done

            half = len(all_connections) / 2 #get half of the total connections

            if che_votes >= half: #if half or more then half 
                msg = 'order placed for cheese pizza' #send cheese message to client
                self.client.send(str.encode(msg))
                print("Cheese has been ordered!") #for server to know order
                 
            elif pep_votes > half: #if more then half
                msg = 'order placed for pepperoni pizza' #send pepperoni message to client
                self.client.send(str.encode(msg))
                print("Pepperoni has been ordered!") #for serevr to knows order

        except:
            print("Error with voting") #prints if error occurs
    
    #in order to close the connection
    def end_conn(self):
        try:
            msg = 'Program is closing, press any key to exit programm\n' #send closing message to client
            self.client.send(str.encode(msg))
            print(f"Sending closing message to {self.address}\n") #for server to know when connection closed

            with mutex: #critical section
                self.connections.remove(self.address) #removes address from the list
            self.client.close()

        except:
            print("Error with closing message") #prints if error occurs here    
        
def main():
    global mutex #initialise mutex
    mutex = threading.Lock()
    
    global all_connections #initialise list
    all_connections = []

    global all_votes
    all_votes = 0

    global che_votes
    che_votes = 0

    global pep_votes
    pep_votes = 0


    host = ""
    port = 9999

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #ipv4 and tcp connection
    server.bind((host, port)) #binding to ip address and port num
    server.listen() #listen for connections

    print("Server listening\n")

    while True:
        client, address = server.accept() #accept connection
        print("Connection from: ", str(address)) #prints address
        with mutex: #critical section
            all_connections.append(address) #add address to the list

        
        c_handler = handle_client(client, address, all_connections) #calling function
        c_handler.start() #start function

if __name__ == "__main__":
    main() #the main
