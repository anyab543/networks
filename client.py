import socket
import threading
import sys

def listen_for_messages(sock):
    while True:
        try:
            # Receive messages
            message = sock.recv(1024).decode()
            if message == '':
                break
            print("\n" + message)
        except OSError:  # Possibly client has left the chat.
            break

def send_messages(sock):
    while True:
        message = input('')
        if message == "!exit":
            # Close the listening thread
            sock.shutdown(socket.SHUT_RD)
            sock.close()
            break
        try:
            sock.sendall(message.encode())
        except OSError:  # Possibly client has left the chat.
            break

def client_program():
    host = '127.0.0.1'  # Server's IP address
    port = 9999  # Server's port number

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    print("Connected to chat server")

    # Start listening for messages from the server
    receive_thread = threading.Thread(target=listen_for_messages, args=(client,))
    receive_thread.start()

    # Start sending messages to the server
    send_messages(client)

if __name__ == '__main__':
    client_program()
