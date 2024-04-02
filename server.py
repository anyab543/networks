import socket
import threading

chat_room = []
voting_room = {}
chat_room_lock = threading.Lock()

def broadcast_message(message, exclude_socket=None):
    with chat_room_lock:
        for client in chat_room:
            if client != exclude_socket:
                client.sendall(message.encode())

class ClientHandler(threading.Thread):
    def __init__(self, client_socket, client_address):
        super().__init__()
        self.client_socket = client_socket
        self.client_address = client_address

    def run(self):
        self.client_socket.sendall("Solve this riddle to enter the chat room: 'Which thing have to be broken before you use it?'".encode())
        answer = self.client_socket.recv(1024).decode().strip().lower()
        if answer == 'egg':
            self.attempt_entry_to_chat()
        else:
            self.client_socket.sendall("Incorrect! Please try again later.".encode())
            self.client_socket.close()

    def attempt_entry_to_chat(self):
        with chat_room_lock:
            if len(chat_room) == 0:
                self.enter_chat()
            else:
                self.client_socket.sendall("Waiting for other clients to vote for your entry...".encode())
                voting_room[self.client_socket] = {'votes': 0, 'total': len(chat_room)}

                # Ask other clients to vote
                broadcast_message(f"Client {self.client_address} is trying to enter the chat room. Type '!yes' to allow, '!no' to deny.")
                while True:
                    # Wait until a decision is made
                    if self.check_votes():
                        break

    def enter_chat(self):
        chat_room.append(self.client_socket)
        self.client_socket.sendall("You are now in the chat room!".encode())
        self.chat()

    def check_votes(self):
        votes_info = voting_room.get(self.client_socket)
        if votes_info and votes_info['votes'] > 0:
            majority = (votes_info['total'] // 2) + 1
            if votes_info['votes'] >= majority:
                del voting_room[self.client_socket]
                self.enter_chat()
                return True
            elif votes_info['votes'] <= -majority:
                self.client_socket.sendall("Entry to the chat room was denied by the current members.".encode())
                self.client_socket.close()
                return True
        return False

    def chat(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                if message == '!exit':
                    self.disconnect_client()
                elif message.startswith('!vote '):
                    self.count_vote(message)
                else:
                    broadcast_message(f"{self.client_address}: {message}")
            except ConnectionResetError:
                self.disconnect_client()

    def count_vote(self, message):
        _, vote, client_id = message.split()
        with chat_room_lock:
            for client in voting_room:
                if str(id(client)) == client_id:
                    voting_room[client]['votes'] += 1 if vote == 'yes' else -1
                    break

    def disconnect_client(self):
        self.client_socket.close()
        with chat_room_lock:
            if self.client_socket in chat_room:
                chat_room.remove(self.client_socket)
            if self.client_socket in voting_room:
                del voting_room[self.client_socket]
        print(f"Client {self.client_address} has disconnected.")

if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen()

    print("Server is running and listening for connections...")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            client_handler = ClientHandler(client_socket, client_address)
            client_handler.start()
    except KeyboardInterrupt:
        print("\nServer is shutting down.")
        with chat_room_lock:
            for client in chat_room:
                client.close()
        server_socket.close()
