import socket
import threading
import random

# Global variables
pizza_item_list = ["Mozzarella", "Cheddar", "Parmesan", "Pepperoni", "Bacon", "Chicken", "Mushrooms", "Onions", "Bell Peppers"]
final_pizza = []
mutex = threading.Lock()
condition = threading.Condition(mutex)
all_connections = []
votes = {item: [] for item in pizza_item_list}  # Tracks votes for each topping

riddles = ["The more of this there is, the less you see. What is it?",
           "Which fish costs the most?",
           "What goes up, but never comes down?",
           "What must be broken before you can use it?",
           "What is full of holes but still holds water?",
           "I am easy to lift, but hard to throw. What am I?"]
riddle_answers = ["darkness",
                  "goldfish",
                  "age",
                  "egg",
                  "sponge",
                  "feather"]


class ClientHandler(threading.Thread):
    def __init__(self, client, address):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address

    def run(self):
        random_index = random.randint(0, len(riddles) - 1)
        self.client.sendall(f"Welcome! Solve this riddle: {riddles[random_index]}\n.".encode())
        if self.solve_riddle(random_index):
            for topping in pizza_item_list:
                self.vote_on_topping(topping)
        final_pizza_msg = 'Your pizza has been created. Your toppings are:'
        for selected_toppings in final_pizza:
            final_pizza_msg = final_pizza_msg + ' ' + selected_toppings + ','
        final_pizza_msg = final_pizza_msg.rstrip(',')
        self.client.sendall(final_pizza_msg.encode())
        self.client.sendall(b". Enjoy!\n\nThank you for participating. Goodbye!\n")
        self.client.close()
        with condition:
            all_connections.remove(self)
            condition.notify_all()  # Notify other threads in case they are waiting for votes

    def solve_riddle(self, riddle_index):
        attempts = 3
        while attempts > 0:
            answer = self.client.recv(1024).decode().strip().lower()
            if answer == riddle_answers[riddle_index]:
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
                if topping not in final_pizza:
                    final_pizza.append(topping)
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
