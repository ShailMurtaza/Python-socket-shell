from __future__ import print_function
from time import sleep as sl
from socket import socket


def connection():
    c = socket()
    host = "127.0.0.1"
    port = 9090
    c.connect((host, port))
    print(c.recv(1024), end='')
    while True:
        cmd = (raw_input(">"))
        if len(cmd) > 0:
            c.send(cmd)
            print(c.recv(9000), end="")


while True:
    try:
        connection()
    except:
        sl(.5)
        print("Retrying .....")
