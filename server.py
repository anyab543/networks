import socket
import threading
import time

# Initialising global variables
mutex = threading.Lock()
all_connections = []
all_votes = 0
yes_votes = 0

class handle_client(threading.Thread):
    def __init__(self, client, address, connections):
        super().__init__()
        self.client = client
        self.address = address
        self.connections = connections
        self.lives = 3

    def run(self):
        self.begin()

    def begin(self):
        try:
            welcome_msg = 'You must solve this riddle in 3 attempts! "The more of this there is, the less you see. What is it?" \n'
            self.client.send(welcome_msg.encode())
            self.riddle('darkness')
        finally:
            self.client.close()

    def riddle(self, answer):
        try:
            while self.lives > 0:
                response = self.client.recv(1024).decode().strip()
                if response.lower() == answer:
                    self.success()
                    return
                else:
                    self.lives -= 1
                    if self.lives == 0:
                        self.fail()
                    else:
                        attempts_msg = f'{self.lives} attempts remaining\n'
                        self.client.send(attempts_msg.encode())
        except Exception as e:
            print("Error with riddle interaction:", e)

    def success(self):
        global all_votes, yes_votes
        try:
            completed_msg = 'Congrats, you solved the riddle! Do you want some information? (yes/no)\n'
            self.client.send(completed_msg.encode())
            response = self.client.recv(1024).decode().strip().lower()
            with mutex:
                all_votes += 1
                if response == 'yes':
                    yes_votes += 1
            self.voting()
        except Exception as e:
            print("Error in success:", e)

    def fail(self):
        fail_msg = 'Failed security test. Press any key to exit program\n'
        self.client.send(fail_msg.encode())
        print("Client failed riddle test")
        with mutex:
            self.connections.remove(self.address)
        self.client.close()

    def voting(self):
        global all_votes, yes_votes
        try:
            while all_votes < len(all_connections):
                time.sleep(1)  # Wait for all votes
            if (yes_votes / len(all_connections)) >= 0.5:
                msg = 'Majority agrees.\n'
            else:
                msg = 'Program is closing, press any key to exit program\n'
            self.client.send(msg.encode())
        except Exception as e:
            print("Error in voting:", e)

    def end_conn(self):
        msg = 'Program is closing, press any key to exit program\n'
        self.client.send(msg.encode())
        with mutex:
            self.connections.remove(self.address)
        self.client.close()

def main():
    host = "127.0.0.1"
    port = 1113  # Ensure this matches the client configuration

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print("Server listening")

    while True:
        client, address = server.accept()
        print("Connection from:", address)
        with mutex:
            all_connections.append(address)
        c_handler = handle_client(client, address, all_connections)
        c_handler.start()

if __name__ == "__main__":
    main()
