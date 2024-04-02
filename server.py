import socket
import threading
import time

# Initialising global variables
mutex = threading.Lock()
all_connections = []
base_options = ["Neapolitan Crust", "New York-Style Crust", "Chicago Deep Dish Crust"]

def collect_votes(option):
    """Collects votes for a given option from all clients."""
    global all_connections
    yes_votes = 0
    no_votes = 0

    for client, _ in all_connections:
        try:
            client.send(f"Do you want {option}? (yes/no)\n".encode())
            response = client.recv(1024).decode().strip().lower()
            if response == "yes":
                yes_votes += 1
            else:
                no_votes += 1
        except Exception as e:
            print(f"Error collecting vote: {e}")
    
    return yes_votes, no_votes

class ClientThread(threading.Thread):
    def __init__(self, client, address):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        self.lives = 3

    def run(self):
        try:
            self.client.send("Solve this riddle: The more of this there is, the less you see. What is it?\n".encode())
            while self.lives > 0:
                answer = self.client.recv(1024).decode().strip().lower()
                if answer == "darkness":
                    self.vote_on_options()
                    break
                else:
                    self.lives -= 1
                    self.client.send(f"Incorrect. {self.lives} attempts left.\n".encode())
            else:
                self.client.send("Failed to solve the riddle. Disconnecting.\n".encode())
        finally:
            self.client.close()

    def vote_on_options(self):
        for option in base_options:
            yes_votes, no_votes = collect_votes(option)
            if yes_votes > no_votes:
                self.client.send(f"Majority chose {option}.\n".encode())
                break
            elif yes_votes == no_votes:
                self.client.send(f"Tie. Choosing {option} by default.\n".encode())
                break
            # If majority says 'no', continue to the next option
        self.client.send("Voting ended. Disconnecting.\n".encode())

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("", 1113))
    server_socket.listen(5)
    print("Server listening...")

    try:
        while True:
            client, address = server_socket.accept()
            print(f"Connection from {address} has been established.")
            with mutex:
                all_connections.append((client, address))
            client_thread = ClientThread(client, address)
            client_thread.start()
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
