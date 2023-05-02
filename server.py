import socket, argparse, os

parser = argparse.ArgumentParser()
parser.add_argument('-a', '--address', type=str,
			default="0.0.0.0",
			help='IP Address to listen on')
parser.add_argument('-p', '--port', type=int, default=65432,
			help='TCP port to listen on')
args = parser.parse_args()

orig_dir = os.getcwd()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.bind((args.address, args.port))
	s.listen()
	print(f"Listening on {args.address}:{args.port}...")
	while True:
		conn, addr = s.accept()
		with conn:
			print(f"Connected by {addr}")
			while True:
				cmd = conn.recv(1024).decode("utf-8")
				if(("list" in cmd.lower()) or ("ls" in cmd.lower())):
					files = "File Listing:\n"
					files += "\n".join([str("\t" + f) for f in os.listdir('.') if os.path.isfile(f)]) + "\n"
					files += "\n".join([str("\t" + f.path) for f in os.scandir(".") if f.is_dir()])
					conn.sendall(bytes(str(len(files)), 'utf-8'))
					conn.recv(3)
					conn.sendall(files.encode('utf-8'))
				elif("get" in cmd.lower()):
					data = conn.recv(1024).decode(encoding="utf-8")
					try:
						with open(data, 'rb') as f:
							file_contents = f.read()
							file_len = len(file_contents)
							header = bytes(str(file_len), 'utf-8')
						conn.sendall(header)
						conn.recv(3)
						conn.sendall(file_contents)
					except:
						conn.sendall("Resource Not Found!".encode("utf-8"))
				elif(("exit" in cmd.lower()) or ("quit" in cmd.lower())):
					os.chdir(orig_dir)
					break
				elif(("cd" in cmd.lower()) or ("chdir" in cmd.lower())):
					os.chdir(conn.recv(1024).decode('utf-8'))
				elif("size" in cmd.lower()):
					data = conn.recv(1024).decode(encoding="utf-8")
					try:
						with open(data, 'rb') as f:
							conn.sendall(bytes(str(len(f.read())), 'utf-8'))
					except:
						conn.sendall("Resource Not Found!".encode("utf-8"))
