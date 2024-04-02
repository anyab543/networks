import socket
import threading

def receive_messages():
    while True:
        try:
            # Receive data from the server
            data = client.recv(1024).decode()
            if 'any key to exit programm' in data:
                # Handle server's prompt for exit
                print('\nServer> ', data)
                input('Press any key to exit...')
                client.close()
                break
            else:
                print('\nServer> ', data)
        except:
            # Handle any exception by breaking the loop to end the thread
            print('You have been disconnected from the server.')
            client.close()
            break

def send_messages():
    while True:
        try:
            # Allow the user to input messages
            message = input('')
            if message.lower() == 'exit':
                # If the user types 'exit', close the connection
                client.send('exit'.encode())
                client.close()
                break
            else:
                # Send the input message to the server
                client.send(message.encode())
        except:
            # Handle any exception by breaking the loop to end the thread
            print('Error sending message.')
            client.close()
            break

# Set up the client connection
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "192.168.1.4" # IP address of the server
port = 12000

# Attempt to connect to the server
try:
    client.connect((host, port))
except:
    print("Connection to the server failed.")
    exit()

# Create a thread for receiving messages from the server
thread_receiving = threading.Thread(target=receive_messages)
thread_receiving.start()

# Call the send_messages function in the main thread to allow user input
send_messages()
