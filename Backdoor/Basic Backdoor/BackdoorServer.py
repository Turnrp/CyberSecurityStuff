import socket
import os
import subprocess

os.chdir(
    "C:\\Users\\"
    + subprocess.run("whoami", stdout=subprocess.PIPE)
    .stdout.decode("utf-8")
    .split("\\")[1]
    .replace("\r\n", "")
)

print(socket.gethostbyname(socket.gethostname()))
s = socket.socket()
port = 8080
s.bind(("", port))

print("Listening...")
s.listen(5)

Bytes = 4096

while True:
    c, addr = s.accept()
    print("Got connection from", addr)

    sent = c.recv(Bytes).decode()
    sending = sent.encode()

    try:
        if "download" in sent:
            with open(sent.replace("download ", ""), "r") as file:
                sendingName = sent.replace("download ", "").split("\\")
                # sending = file.read().encode()
                sending = (
                    "file: "
                    + sendingName[len(sendingName) - 1]
                    + " : "
                    + "\n".join(file.read().splitlines())
                ).encode()
        elif "upload" in sent:
            Name = sent.replace("upload", "").split(" ")[1]
            Contents = sent.replace("upload", "").split(" ", 2)[2]
            with open(Name, "w") as file:
                file.write(Contents)
            sending = "Uploaded Sucessfully.".encode()
        elif "[GetDIR]" in sent:
            # print("sending dir")
            sending = ("DIR: " + os.curdir).encode()
        elif "print" in sent:
            File = sent.replace("print ", "")
            sending = (open(File, "r").read()).encode()
        elif "dir" in sent:
            sending = "\n".join(os.listdir()).encode()
        elif "cd" in sent:
            os.chdir(sent.replace("cd ", ""))
            sending = ("DIR: " + sent.replace("cd ", "")).encode()
        elif "get" in sent:
            sent = sent.replace("get ", "")
            if "size" in sent:
                sent = sent.replace("size ", "")
                sending = str(os.path.getsize(sent)).encode()
        elif "set" in sent:
            sent = sent.replace("set ", "")
            if "bytes" in sent:
                print("Setting bytes..")
                sent = sent.replace("bytes ", "")
                Bytes = int(sent)
                sending = "Successfully changed Byte Size.".encode()
        else:
            try:
                result = subprocess.run(sent, stdout=subprocess.PIPE)
                sending = result.stdout
            except FileNotFoundError:
                sep = sent.split(" ", 2)
                # print(sep)
                command = "start " + sep[0] + " " + os.curdir + "\\" + sep[1]
                result = subprocess.run(
                    command,
                    stdout=subprocess.PIPE,
                    shell=True,
                    # creationflags=subprocess.CREATE_NEW_CONSOLE,
                )
                sending = result.stdout
    except Exception as e:
        sending = str(e).encode()

    c.send(sending)
