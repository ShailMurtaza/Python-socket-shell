from __future__ import print_function
from socket import socket, error


def connection():
    s = socket()
    host = ""
    port = 9090
    s.bind((host, port))
    s.listen(1)
    print("Listening ......")
    conn, address = s.accept()
    print("Connected with " + str(address))
    print(conn.recv(1024), end="")
    while True:
        cmd = (raw_input(">"))
        if len(cmd) > 0:
            conn.send(cmd)
            print(conn.recv(9000), end="")


while True:
    try:
        connection()
    except error as msg:
        print(msg)
        print("Retrying ...")
