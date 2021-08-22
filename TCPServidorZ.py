import socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((socket.gethostname(),5100))
print(socket.gethostname())
serverSocket.listen(1)
print('The server is ready to receive')
while 1:
    clientsocket, address = serverSocket.accept()
    sentence = clientsocket.recv(1024)
    capitalizedSentence = (sentence.decode("utf-8")).upper()
    clientsocket.send(bytes(capitalizedSentence, "utf-8"))
    clientsocket.close()