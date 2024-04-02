import socket
import threading

# Global variables for managing connections and votes
connections = []
pepperoni_votes = {'yes': 0, 'no': 0}
margarita_votes = {'yes': 0, 'no': 0}
vote_lock = threading.Lock()

class HandleClient(threading.Thread):
    def __init__(self, client, address):
        super().__init__()
        self.client = client
        self.address = address

    def run(self):
        self.send_riddle()
        self.ask_pizza_preference()

    def send_riddle(self):
        riddle = 'Solve this riddle: "The more of this there is, the less you see. What is it?" Answer: darkness\n'
        self.client.send(riddle.encode())
        # Expecting the client to respond with the answer, but not validating here for brevity

    def ask_pizza_preference(self):
        # Ask about pepperoni pizza
        pepperoni_question = "Do you guys want pepperoni pizza (yes/no)?"
        self.ask_question(pepperoni_question, pepperoni_votes)

        with vote_lock:
            if sum(pepperoni_votes.values()) == len(connections):  # Ensure all have voted
                if pepperoni_votes['yes'] > pepperoni_votes['no']:
                    self.broadcast_message("Here is your Pepperoni pizza.")
                    return

        # If not enough 'yes' votes for pepperoni, ask about Margarita pizza
        margarita_question = "Would you guys like Margarita pizza (yes/no)?"
        self.ask_question(margarita_question, margarita_votes)

        with vote_lock:
            if sum(margarita_votes.values()) == len(connections):  # Ensure all have voted
                if margarita_votes['yes'] > margarita_votes['no']:
                    self.broadcast_message("Here is your Margarita pizza.")
                else:
                    self.broadcast_message("Disconnecting all clients...")

    def ask_question(self, question, votes_dict):
        self.client.send(question.encode())
        while True:  # Keep asking until a valid response is received
            response = self.client.recv(1024).decode().strip().lower()
            if response in votes_dict:  # Check if the response is 'yes' or 'no'
                with vote_lock:
                    votes_dict[response] += 1
                break  # Exit the loop after receiving a valid response
            else:
                self.client.send(b"Please answer 'yes' or 'no': ")  # Prompt again for a valid response


    def broadcast_message(self, message):
        for client, _ in connections:
            client.send(message.encode())

def accept_connections(server):
    while True:
        client, address = server.accept()
        print(f"Connection from {address}")
        with vote_lock:
            connections.append((client, address))
        handler = HandleClient(client, address)
        handler.start()

def main():
    host = '0.0.0.0'
    port = 1113  # The port number should match what is expected by the client scripts

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    print(f"Server listening on {host}:{port}")
    accept_connections(server)

if __name__ == "__main__":
    main()
