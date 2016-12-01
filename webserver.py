import socket
import sys

class WebServer:
	
	def __init__(self, port=8080):
		self.port = port
		self.directory = 'contents'
		self.ipAddress = '127.0.0.1'

	def createSocket(self):
		self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			self.serverSocket.bind((self.ipAddress, self.port))
			greenColor = '\033[92m'
			whiteColor = '\033[0m'
			print(greenColor + "Starting up http-server, serving ./")
			print("Available on\n http://127.0.0.1:%d"%self.port)
			print("Hit CTRL-C to stop the server" + whiteColor)
		except:
			self.port += 1
			self.createSocket()
		self.listen()

	def listen(self):
		while(True):
			self.serverSocket.listen(1)
			connectionSocket, clientAddress =  self.serverSocket.accept()
			requestedData = connectionSocket.recv(1024)
			requestedString = bytes.decode(requestedData)
			requestedMethod = requestedString.split(' ')[0]
			print(requestedMethod)
			if(requestedMethod == 'GET'):
				requestedFile = requestedString.split(' ')[1]				
				print(requestedFile)
				if(requestedFile == '/'):
					requestedFile = '/index.html'
				requestedFile = self.directory + requestedFile
				print(requestedFile)
				try:
					fp = open(requestedFile, 'rb')
					responseData = fp.read()
					header = self.headers(200)
					fp.close()
				except:
					header = self.headers(400)
					responseData = b"<html><body><p> Error 404 File not found</p></body></html>"	
				finalResponse = header.encode()
				finalResponse += responseData
				connectionSocket.send(finalResponse)				  
				connectionSocket.close()
			else:
				print("HTTP request methode unknown")			
			
	def headers(self, httpCode):
		headr = ''
		if(httpCode == 200):
			headr = 'HTTP/1.1 200 OK'
		elif(httpCode == 404):
			headr = 'HTTP/1.1 404 File Not Found'
		return headr
	

new_server = WebServer()
new_server.createSocket()
