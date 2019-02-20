import socket


HOST = '127.0.0.1';
PORT = 65432;
simultaneousConnections = 128;

BAD_REQUEST = 'HTTP/1.0 400 Bad Request';
NOT_FOUND = 'HTTP/1.0 404 Not Found';
STATUS_OK = 'HTTP/1.0 200 OK';

mySocket = socket(AF_INET, SOCK_STREAM);
print "Socket successfully created...";

mySocket.bind((HOST, PORT));
mySocket.listen();
print "Server is listening...";

while 1:

	client, addr = mySocket.accept();

	if client:
		print "CLIENT: ", client, "ADDRESS: ", addr;

	received = client.recv(1024);
	receivedStrings = received.split();
	print received;
