import socket
import threading
import sys

def listen_for_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode()
            if message.startswith("Client"):
                print(message)
                print("Enter '!yes' or '!no' followed by the client's address to cast your vote.")
            else:
                print("\n" + message)
        except:
            print("Error receiving data.")
            sock.close()
            sys.exit(0)

def send_messages(sock):
    while True:
        message = input()
        if message == "!exit":
            sock.sendall(message.encode())
            break
        else:
            sock.sendall(message.encode())

    sock.close()
    sys.exit(0)

if __name__ == "__main__":
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 12345))

        threading.Thread(target=listen_for_messages, args=(client_socket,), daemon=True).start()

        riddle_answer = input("Answer the riddle: ")
        client_socket.sendall(riddle_answer.encode())

        send_messages(client_socket)
    except ConnectionRefusedError:
        print("Could not connect to server.")
    except KeyboardInterrupt:
        print("\nClient shutdown.")
    finally:
        client_socket.close()
