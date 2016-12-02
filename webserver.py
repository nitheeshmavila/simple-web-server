import socket
import sys
import time

class HttpServer:
	
	def __init__(self, port=8080):
		self.port = port
		self.host_dir = '.' 
		self.ip_address = '127.0.0.1'

	def create_socket(self):
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			self.server.bind((self.ip_address, self.port))
			green_color = '\033[92m'
			white_color = '\033[0m'
			print(green_color + "Starting up http-server, serving ./")
			print("Available on\n http://127.0.0.1:%d"%self.port)
			print(white_color + "Hit CTRL-C to stop the server" + white_color)
		except:
			self.port += 1
			self.create_socket()
		self.listen()

	def listen(self):
		while True:
			print("Waiting for new connection\n")
			self.server.listen(1)
			conn_socket, address =  self.server.accept()
			requested_data = conn_socket.recv(1024)
			print("Recived connection from:",address)
			requested_string = bytes.decode(requested_data)
			requested_method = requested_string.split(' ')[0]
			print("Request method:",requested_method)
	#		print("Request content:\n",requested_string)
			if(requested_method == 'GET'):
				requested_file = requested_string.split(' ')[1]
				if(requested_file == '/'):
					requested_file = '/index.html'
				requested_file = self.host_dir + requested_file
				try:
					fp = open(requested_file, 'rb')
					response_data = fp.read()
					fp.close()
		#			print("response content:",response_data)
					content_type = self.get_content_type(requested_file)
					header = self.make_header(200, content_type)
				except:
					header = self.make_header(400, 'text/html')
					response_data = "<html><body><p> Error 404 File not found</p></body></html>".encode()	
				final_response = header.encode()
				final_response += response_data
				print("Response:",final_response)
				conn_socket.send(final_response)				  
				conn_socket.close()
			else:
				print(requested_method)
				print("HTTP request method unknown")			
			
	def make_header(self, http_code, content_type):
		headr = ''
		if(http_code == 200):
			headr = 'HTTP/1.1 200 OK\n'
		elif(http_code == 404):
			headr = 'HTTP/1.1 404 File Not Found\n'
		date = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
		headr += 'Date:' + date + '\n'
		headr += 'Server: Python-http-server\n'
		headr += 'Content-Type:'+ content_type + '\n'
		headr += '\n'
		return headr

	def get_content_type(self, file_name):
		content_types = {'html': 'text/html',
						'txt': 'text/txt',
						'jpg': 'image/jpeg',
						'png': 'image/png',
						'ico': 'icon/ico'}
		return content_types[file_name.split('.')[-1]]
			

		
new_server = HttpServer()
new_server.create_socket()


