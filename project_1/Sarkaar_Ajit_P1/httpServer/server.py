import socket
import os
import sys

# CURRENT DIRECTORY PATH
currentPath = os.path.dirname(os.path.abspath(__file__));

# COUNTER FOR NUMBER OF CLIENTS SERVED.
counter = 0;

# TAKE INPUT FROM THE USER FOR THE IP ADDRESS AND PORT NUMBER THE SERVER SHOULD RUN ON.
HOST = raw_input("PLEASE ENTER SERVER IP ADDRESS: ");
PORT = raw_input("PLEASE ENTER SERVER PORT NUMBER: ");
PORT = int(PORT);
# HOST = '127.0.0.1';
# PORT = 65432;

# NUMBER OF SIMULTANEOUS CONNECTIONS SUPPORTED.
simultaneousConnections = 128;

# FORMING RESPONSE MESSAGES TO SEND TO CLIENTS.
BAD_REQUEST = 'HTTP/1.0 400 Bad Request';
NOT_FOUND = 'HTTP/1.0 404 Not Found';
STATUS_OK = 'HTTP/1.0 200 OK\r\n';

# CREATING SOCKET.
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
print "Socket successfully created...";
mySocket.bind((HOST, PORT));

# SERVER SET UP AND LISTENS FOR INCOMING CONNECTIONS.
mySocket.listen(simultaneousConnections);
print "Server is listening...";

# INFINITE LOOP TO SERVE CLIENTS.
while 1:

	# ACCEPTING NEW CLIENT CONNECTIONS.
	client, addr = mySocket.accept();
	
	counter += 1;
	print "Serving Customer No. ", counter;

	# RECEIVING DATA FROM CLIENTS, SUCH AS REQUESTS.
	incoming = client.recv(1024);
	received = incoming;

	receivedStrings = received.split();
	# print receivedStrings;

	# FIRST CHECK OF REQUEST FORMAT AND IF ANY PART OF THE REQUEST IS MISSING.
	if len(receivedStrings) > 2:

		httpMethod = receivedStrings[0];

		# EXTRACTING THE FILE NAME FROM THE REQUEST.
		fileRequestPath = receivedStrings[1];
		fileName = fileRequestPath[1:];

		httpVersion = receivedStrings[2];

		responseBody = '';

		# CHECKING IF THE FORMAT OF THE REQUEST IS CORRECT.
		if httpMethod == "GET" and httpVersion == "HTTP/1.0" and len(fileName) > 0:
			if os.path.isfile(fileName):
				print "File Present...";

				# CHECKING IF USER IS ASKING FOR AN IMAGE.
				if fileName.find('.png') > 0 or fileName.find('.jpg') > 0 or fileName.find('.jpeg') > 0:
					img = open(fileName, 'r');
					fileSize = sys.getsizeof(img);
					print "File Size: ", fileSize;

					responseHeader = STATUS_OK + "\n" + "Content-Length: " + str(fileSize) + "\r\n\r\n";
					
					#SEND RESPONSE THAT IMAGE EXISTS, AND SEND THE IMAGE AFTER THE 200 OK STATUS RESPONSE.
					client.send(responseHeader);

					while True:
						imgData = img.readline(1024);
						if not imgData:
							break;
						client.send(imgData);
				
				# CHECK FOR FILES WHICH ARE NOT IMAGES.
				else:
					f = open(fileName, 'r');
					if f.mode == 'r':
						content = f.read();

					fileSize = sys.getsizeof(content);
					print "File Size: ", fileSize;

					# SEND RESPONSE AND SIZE OF THE OBJECT.
					responseHeader = STATUS_OK + "\n" + "Content-Length: " + str(fileSize) + "\r\n\r\n";
					responseBody = content;
					while True:
						content = f.readline(1024);
						if not content:
							break;
						
						client.send(content);

			# FILE NOT FOUND RESPONSE.
			else:
				responseHeader = NOT_FOUND;
				response = responseHeader + responseBody;
				client.send(response);
		# BAD REQUEST RESPONSE.
		else:
			responseHeader = BAD_REQUEST;
			response = responseHeader + responseBody;
			client.send(response);

		# SEND RESPONSE IF FILE QUERIED FOR IS NOT AN IMAGE.
		# if not(fileName.find('.png') > 0 or fileName.find('.jpg') > 0 or fileName.find('.jpeg') > 0):
		

	# CLOSE THIS CLIENT CONNECTION.	
	client.close();
		# break;	

	
# STOP SERVER ON THIS PORT.
mySocket.close();

