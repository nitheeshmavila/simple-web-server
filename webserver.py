import socket
import sys


class WebServer:
	
	def __init__(self, port):
		self.port = port
		self.directory = 'contents'
		self.ipAddress = '127.0.0.1'

	def createSocket(self):
		self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			self.serverSocket.bind((self.ipAddress, self.port))
			print("Starting HTTP Server in python on ",self.ipAddress,":", self.port)
		except:
			print("Port already in use")
		self.listen()

	def listen(self):
		while(True):
			self.serverSocket.listen(1)
			connectionSocket, clientAddress =  self.serverSocket.accept()
			requestedData = connectionSocket.recv(1024)
			requestedString = bytes.decode(requestedData)
			requestedMethod = requestedString.split(' ')[0]
			if(requestedMethod == 'GET'):
				requestedFile = requestedString.split(' ')[1]				
				if(requestedFile == '/'):
					requestedFile = '/index.html'
				requestedFile = self.directory + requestedFile
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
	

new_server = WebServer(8033)
new_server.createSocket()
