import socket
import threading

# Global variables for the chat room and thread safety
chat_room = []
chat_room_lock = threading.Lock()

class handle_client(threading.Thread):
    def __init__(self, client, address):
        super().__init__()
        self.client = client
        self.address = address
        self.is_in_chat_room = False

    def run(self):
        self.send_riddle()

    def send_riddle(self):
        try:
            welcome_msg = 'Solve this riddle: "What thing have to be broken before you use it?"\n'
            self.client.send(welcome_msg.encode())
            self.handle_riddle_answer()
        except Exception as e:
            print(f"Error handling riddle for {self.address}: {e}")
        finally:
            if not self.is_in_chat_room:
                self.client.close()

    def handle_riddle_answer(self):
        correct_answer = "Egg"
        while True:
            response = self.client.recv(1024).decode().strip()
            if response.lower() == correct_answer.lower():
                self.client.send("Correct! Welcome to the chat room. Type '!exit' to leave.\n".encode())
                self.enter_chat_room()
                break
            else:
                self.client.send("Incorrect. Try again.\n".encode())

    def enter_chat_room(self):
        self.is_in_chat_room = True
        with chat_room_lock:
            chat_room.append(self.client)
        try:
            while True:
                msg = self.client.recv(1024).decode()
                if msg == '!exit':
                    raise Exception("Client left the chat room")
                else:
                    self.broadcast_message(msg)
        except:
            with chat_room_lock:
                chat_room.remove(self.client)
            self.client.close()

    def broadcast_message(self, message):
        with chat_room_lock:
            for client in chat_room:
                if client != self.client:
                    try:
                        client.send(f"{self.address}: {message}\n".encode())
                    except:
                        client.close()
                        chat_room.remove(client)

def main():
    host = '0.0.0.0'
    port = 9999
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    print("Server listening for connections...")

    try:
        while True:
            client, address = server.accept()
            print(f"Connection from: {address}")
            client_handler = handle_client(client, address)
            client_handler.start()
    except KeyboardInterrupt:
        print("Server shutting down.")
    finally:
        server.close()

if __name__ == "__main__":
    main()
