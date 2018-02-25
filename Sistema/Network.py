import socket
import threading
import time

class NetworkServerSocket:
	def __init__(self, host=None, port=5555, maxConnections=5):
		self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		if host == None or not host:
			self.host = socket.gethostname()
		else:
			self.host = host
		self.port = port
		self.serverSocket.bind((self.host, self.port))
		self.serverSocket.listen(maxConnections)
		self.running = True
		t = threading.Thread(target=self.Listen)
		t.start()

	def Listen(self):
		while self.running:
			time.sleep(0.5)
			clientSocket, addr = self.serverSocket.accept()
			data = clientSocket.recv(1024).decode()
			if data == "Stop":
				print("Deteniendo el hilo!")
				self.Stop()
			else:
				print("Received {0}".format(data))
			clientSocket.send("Complete".encode())

	def Stop(self):
		self.running = False
		time.sleep(4)
		self.serverSocket.close()

if __name__ == '__main__':
	v = NetworkServerSocket(host="127.0.0.1", port=5556)