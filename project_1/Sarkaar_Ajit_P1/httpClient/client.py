import socket
import os

# CURRENT DIRECTORY PATH
currentPath = os.path.dirname(os.path.abspath(__file__));

# TAKE INPUT FROM THE USER FOR THE IP ADDRESS AND PORT NUMBER OF THE SERVER.
SERVER = raw_input("PLEASE ENTER SERVER IP ADDRESS: ");
PORT = raw_input("PLEASE ENTER SERVER PORT NUMBER: ");
PORT = int(PORT);

# SERVER = '127.0.0.1';
# PORT = 12010;

# CREATING SOCKET.
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
print "Socket successfully created...";

clientSocket.connect((SERVER, PORT));
print "Request sent to server...";

# FOR META DATA FOR THE REQUEST TO SERVER.
metaDataBefore = "GET /";
metaDataAfter = " HTTP/1.0\r\n\r\n";

# ASKING THE USER FOR FILE NAME TO BE FETCHED.
fileRequest = raw_input("TYPE THE FILE NAME YOU WANT TO FETCH: ");

# FORMING REQUEST.
request = metaDataBefore + fileRequest + metaDataAfter;
# print "REQUEST: ", request;

encodedRequest = request.encode();
checkRes = 0;

# SENDING THE REQUEST AND RECEIVING DATA IS IMAGE IS REQUESTED.
if fileRequest.find('.png') > 0 or fileRequest.find('.jpg') > 0 or fileRequest.find('.jpeg') > 0:
	clientSocket.send(encodedRequest);
	incomingMeta = clientSocket.recv(1024);
	
	print "RESPONSE: ", incomingMeta;
	if incomingMeta.find('HTTP/1.0 404 Not Found') < 0:
		
		fName = raw_input("ENTER FILE NAME FOR IMAGE: ");
		fp = open(fName,'w');
		while True:
			data = clientSocket.recv(1024);

			print "DATA: ", data;

			# if data.find('HTTP/1.0 200 OK') < 0 and checkRes == 0:
			# 	print "RESOURCE NOT RETURNED. CLOSING CONNECTION";
			# 	checkRes += 1;
			# 	break;
			
			if not data:
				break;
			fp.write(data);

# SENDING THE REQUEST AND RECEIVING DATA IS IMAGE IS NOT REQUESTED.
else:
	received = '';
	status = False;
	clientSocket.send(encodedRequest);
	fileRequestToSave = raw_input("ENTER FILE NAME TO SAVE AS: ");
	while True:
		data = clientSocket.recv(1024);

		# print "DATA: ", data;

		# if data.find('HTTP/1.0 200 OK') < 0 and checkRes == 0:
		# 	print "RESOURCE NOT RETURNED. CLOSING CONNECTION";
		# 	checkRes += 1;
		# 	break;
		
		if not data:
			break;
		received = received + str(data);

	if received:
		print "RECEIVED: \n", received;
		
		textFile = open(fileRequestToSave + ".txt", "w");
		if len(received.split('\r\n\r\n')) > 1:
			dataToSave = received.split('\r\n\r\n')[1];
			# print "dataToSave: ", dataToSave;
			textFile.write(dataToSave);
			textFile.close();

# CLOSING THE CONNECTION.
clientSocket.close(); 

