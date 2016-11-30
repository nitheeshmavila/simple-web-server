import socket
import sys

def create_socket():
	server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_sock.bind(('127.0.0.1', 8087))
	server_sock.listen(1)
	return server_sock



server_sock = create_socket()
while True:
	conn, address = server_sock.accept()
	request = conn.recvfrom(1024)
	print(request)
	http_response = """\
					HTTP/1.1 200 OK
					Hello World!
					"""
	conn.sendall(http_response.encode('utf-8'))
	conn.close()

