import socket

# Function to connect to the server (peer) and send a message
def connect_to_server(server_address):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Ipv4 and tcp connection
    client_socket.connect(server_address)

    while True:
        print("Send message or type 'bye' to end connection: ")
        message = input()

        if message.lower() == 'bye':
            break 

        client_socket.send(message.encode())
        response = client_socket.recv(1024)
        print(f"Response from server: {response.decode()}")
    client_socket.close()


# Example usage
if __name__ == "__main__":
    server_address = ('172.27.107.120', 1200)  # Change depending on address
    #message = "Hi from this client!"
    connect_to_server(server_address)
