import socket
from os.path import getsize, exists
from os import listdir

IP = "127.0.0.1"  # input("Input IP to connect to: ")
PORT = 8080  # int(input("Input Port to connect to: "))
hasConnected = False
curDir = ""
Bytes = 4096

while 1:
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((IP, PORT))

    if not hasConnected:
        connection.send("[GetDIR]".encode())
        curDir = connection.recv(Bytes).decode().replace("DIR: ", "")
        connection.close()
        hasConnected = True
    else:
        command = input(
            str(connection.getsockname()[0])
            + "@"
            + str(connection.getsockname()[1])
            + ":"
            + curDir
            + "-$ "
        )

        if command == "exit":
            connection.close()
            break
        elif "upload" in command:
            Name = command.replace("upload", "").split(" ")[1]
            if exists(Name):
                Contents = open(Name, "r").read()
            else:
                Contents = command.replace("upload", "").split(" ", 2)[2]
            command = "upload " + Name + " " + Contents

        if command == "":
            command = "NULL"
        else:
            # print(command)
            connection.send(command.encode())
            response = connection.recv(Bytes).decode()

        if "file: " in response:
            response = response.replace("file: ", "").split(" : ", 1)
            print(response)
            with open(response[0], "w") as file:
                file.write(response[1])
            print(response[0], "Has been downloaded.")
        elif "DIR:" in response:
            curDir = response.replace("DIR: ", "")
            print(response)
        elif "set" in command:
            command = command.replace("set ", "")
            if "bytes" in command:
                print("Setting bytes..")
                command = command.replace("bytes ", "")
                Bytes = int(command)
        elif "get" in command:
            command = command.replace("get ", "")
            if "bytes" in command:
                # command = command.replace("bytes ", "")
                print(Bytes)
            elif "size" in command:
                if exists(command.replace("size ", "")):
                    print(getsize(command.replace("size ", "")))
                else:
                    print(response)
            else:
                print(response)
        elif command == "selfdir":
            print("\n".join(listdir()))
        else:
            print(response)
    connection.close()
