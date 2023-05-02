import socket, argparse

auth = False

parser = argparse.ArgumentParser()
parser.add_argument('-a', '--address', type=str,
			default="0.0.0.0",
			help='IP Address to connect to')
parser.add_argument('-p', '--port', type=int, default=65432,
			help='TCP port to connect on')
args = parser.parse_args()

file_contents = bytes()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((args.address, args.port))
	
	if auth:
		while True:
			uname = input("Username? ")
			s.sendall(uname.encode('utf-8'))
			s.recv(3)
			pword = input("Pword? ")
			s.sendall(pword.encode('utf-8'))
			code = s.recv(1)
			if(code == b'S'):
				break
			else:
				print("Bad Credentials")

	while True:
		comm = input("Command ?")
		s.sendall(comm.encode('utf-8'))
		if(("list" in comm.lower()) or ("ls" in comm.lower())):
			sbuf = ""
			l = int(s.recv(64).decode('utf-8'))
			s.sendall(b"ACK")
			while len(sbuf) < l:
				sbuf += s.recv(1028).decode('utf-8')
				print(sbuf)
		elif("get" in comm.lower()):
			file_contents = bytes()
			file_name = input("Enter File Name> ")
			s.sendall(bytes(file_name, 'utf-8'))
			header_data = s.recv(1024).decode(encoding='utf-8')
			try:
				file_len = int(header_data)				
			except:
				print("File does not exist on server.")
			try:
				s.sendall(b'ACK')
				while len(file_contents) < file_len:
					file_contents += s.recv(1024)
					print(len(file_contents) / file_len)
				with open(file_name, "wb") as f:
					f.write(file_contents)
			except:
				print(end='')
		elif(("exit" in comm.lower()) or ("quit" in comm.lower())):
			print("Goodbye!")
			exit()
		elif(("?" in comm.lower()) or ("help" in comm.lower())):
			print("COMMANDS:\nLS/LIST - LIST FILES")
			print("GET - GET FILE FROM SERVER")
			print("CD/CHDIR - CHANGE DIRECTORY")
			print("EXIT/QUIT - TERMINATE CONNECTION")
			print("SIZE - GET FILE SIZE IN BYTES")
		elif(("cd" in comm.lower()) or ("chdir" in comm.lower())):
			dir = input("Enter directory to enter> ")
			s.sendall(bytes(dir, 'utf-8'))
		elif("size" in comm.lower()):
			file_name = input("Enter File Name> ")
			s.sendall(bytes(file_name, 'utf-8'))
			header_data = s.recv(1024).decode(encoding='utf-8')
			print(header_data)
