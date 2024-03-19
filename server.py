import socket
import threading

# Function to handle incoming connections
def connection(client_socket, address):
    print(f"Accepted connection from {address}")
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        if data.lower().strip() == 'bye':
            break   
        caps = data.upper()
        client_socket.send(caps)

    client_socket.close()
    print(f"Connection closed with {address}")

# Function to start listening for incoming connections
def start_server():
    host = '172.27.107.120'
    port = 1200

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Server listening on {host} : {port}")

    while True:
        client_socket, address = server_socket.accept()
        client_handler = threading.Thread(target=connection, args=(client_socket, address))
        client_handler.start()

# Function to connect to other peers
def connect_to_peer(peer_address, message):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(peer_address)
    client_socket.send(message.encode())
    response = client_socket.recv(1024)
    print(f"Received response from {peer_address}: {response.decode()}")
    client_socket.close()

if __name__ == "__main__":
    # Start server in a separate thread
    server_thread = threading.Thread(target=start_server)
    server_thread.start()
