import socket
import threading

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
            welcome_msg = 'You must solve this riddle in 3 attempts! "What question can you never answer yes to?" \n'
            self.client.send(str.encode(welcome_msg))
            print("Riddle sent\n")
            answer = 'are you asleep yet?'
            self.riddle(answer)
        finally:
            self.client.close()

    def riddle(self, answer):
        try:
            while self.lives >= 1:
                response = self.client.recv(1024)
                if response.decode().lower() == answer:
                    self.success()
                    return
                else:
                    self.lives -= 1
                    if self.lives == 0:
                        self.fail()
                    else:
                        attempts = f'{self.lives} attempts remaining\n'
                        self.client.send(str.encode(attempts))
        except Exception as e:
            print("Error with sending riddle message: \n", e)

    def success(self):
        try:
            completed = 'Congrats you solved the riddle! Do you want to chat with others? yes/no\n'
            self.client.send(str.encode(completed))
            response = self.client.recv(1024)
            if response.decode().lower() == 'yes':
                self.service()
            else:
                self.end_conn()
        except:
            print("Error with success message")

    def fail(self):
        try:
            fail = 'Failed security test. Press any key to exit programm\n'
            self.client.send(str.encode(fail))
            print("Client failed riddle test")
            with mutex:
                if self.address in self.connections:
                    self.connections.remove(self.address)
            self.client.close()
        except:
            print("Error with fail message")

    def broadcast(self, message):
        for client in self.connections:
            if client != self.client:
                try:
                    client.send(message)
                except:
                    client.close()
                    with mutex:
                        self.connections.remove(client)

    def service(self):
        try:
            chat_message = 'Welcome to the chat! Type "exit" to leave.\n'
            self.client.send(str.encode(chat_message))
            while True:
                msg = self.client.recv(1024)
                if msg.decode().lower() == 'exit':
                    break
                broadcast_message = f"Message from {self.address}: {msg.decode()}\n"
                self.broadcast(str.encode(broadcast_message))
        except Exception as e:
            print(f"Error in chat service with {self.address}: {e}")
        finally:
            self.end_conn()

    def end_conn(self):
        try:
            msg = 'Exiting chat room, press any key to exit programm\n'
            self.client.send(str.encode(msg))
            print(f"Client {self.address} exiting")
            with mutex:
                if self.client in self.connections:
                    self.connections.remove(self.client)
            self.client.close()
        except Exception as e:
            print(f"Error closing connection with {self.address}: {e}")

def main():
    global mutex, all_connections
    mutex = threading.Lock()
    all_connections = []

    host = ""
    port = 12000

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    print("Server listening for connections...")

    while True:
        client, address = server.accept()
        print(f"Connection from: {address}")
        with mutex:
            all_connections.append(client)

        c_handler = handle_client(client, address, all_connections)
        c_handler.start()

if __name__ == "__main__":
    main()
