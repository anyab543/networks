import socket
import threading

# Global variables
pizza_item_list = ["Mozzarella", "Cheddar", "Parmesan", "Pepperoni", "Bacon", "Chicken", "Mushrooms", "Onions", "Bell Peppers"]
mutex = threading.Lock()
condition = threading.Condition(mutex)
all_connections = []
votes = {item: [] for item in pizza_item_list}  # Tracks votes for each topping

class ClientHandler(threading.Thread):
    def __init__(self, client, address):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address

    def run(self):
        self.client.sendall(b"Welcome! Solve this riddle: The more of this there is, the less you see. What is it?\n")
        if self.solve_riddle():
            for topping in pizza_item_list:
                self.vote_on_topping(topping)
        self.client.sendall(b"Thank you for participating. Goodbye!\n")
        self.client.close()
        with condition:
            all_connections.remove(self)
            condition.notify_all()  # Notify other threads in case they are waiting for votes

    def solve_riddle(self):
        attempts = 3
        while attempts > 0:
            answer = self.client.recv(1024).decode().strip().lower()
            if answer == "darkness":
                self.client.sendall(b"Correct! Let's build your pizza.\n")
                return True
            else:
                attempts -= 1
                self.client.sendall(f"Incorrect. {attempts} attempts left.\n".encode())
        return False

    def vote_on_topping(self, topping):
        self.client.sendall(f"Do you want to add {topping} to your pizza? (yes/no)\n".encode())
        vote = self.client.recv(1024).decode().strip().lower()
        
        with condition:
            votes[topping].append(vote)
            condition.notify_all()  # Notify other threads that a vote has been cast
            # Wait until all clients have voted
            while len(votes[topping]) < len(all_connections):
                condition.wait()

        yes_votes = votes[topping].count('yes')
        if yes_votes > len(all_connections) / 2:
            with condition:
                self.client.sendall(f"Ingredient Added: {topping}\n".encode())
        else:
            with condition:
                self.client.sendall(f"Ingredient Not Added: {topping}\n".encode())

        with condition:
            # Reset votes for this topping for the next round
            if all(len(votes[t]) == len(all_connections) for t in pizza_item_list):
                votes[topping] = []

def accept_connections(server):
    while True:
        client, address = server.accept()
        print(f"Connection from {address}")
        client_handler = ClientHandler(client, address)
        with condition:
            all_connections.append(client_handler)
            condition.notify_all()  # Notify other threads in case they are waiting for more connections
        client_handler.start()

def main():
    host = ''
    port = 1113
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Server listening on port {port}")
    accept_connections(server)

if __name__ == "__main__":
    main()
