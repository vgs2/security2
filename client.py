#!/usr/bin/env python3

import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    while(True):
        data = input('Digite o comando desejado (digite help para obter orientações)\n')
        s.connect((HOST, PORT))
        s.sendall(bytes(data.encode()))
        data = s.recv(1024)
        print(data.decode())
