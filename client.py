import socket
from ZVprotect import ZVprotect as ZV
import pickle

CLIENT_PRIVATE_KEY_PATH = 'keys/client1_private_key.key'
CLIENT_PUBLIC_KEY_PATH = 'keys/client1_public_key.key'
SERVER_PUBLIC_KEY_PATH = 'keys/server_public_key.key'
N_SERVER_PATH = 'keys/n.key'
N_CLIENT_PATH = 'keys/client1n.key'

with open(CLIENT_PRIVATE_KEY_PATH, 'rb') as fp:
    client_private_key = pickle.load(fp)
with open(CLIENT_PUBLIC_KEY_PATH, 'rb') as fp:
    client_public_key = pickle.load(fp)
with open(SERVER_PUBLIC_KEY_PATH, 'rb') as fp:
    server_public_key = pickle.load(fp)
with open(N_SERVER_PATH, 'rb') as fp:
    n_server = pickle.load(fp)
with open(N_CLIENT_PATH, 'rb') as fp:
    n_client = pickle.load(fp)
print(n_client)


clientSocket = ZV.Conexao.conectar(modo=1)
clientSocket.send(bytes(str(client_public_key), "utf-8"))
# clientSocket.send(bytes(str(n_client), "utf-8"))
clientSocket.send(bytes(n_client))
ZV.Envio.enviar(clientSocket, 'votar', 'carro', server_public_key, client_private_key, n_server, ZV.CAssimetrica.gerarChaves()[3])
# clientSocket.send(bytes(capitalizedSentence, "utf-8"))





# clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# clientSocket.connect((socket.gethostname(),5100))
# sentence = input('lowercase sentence:')
# clientSocket.send(bytes(sentence, "utf-8"))
# modifiedSentence = clientSocket.recv(1024)
# print('From Server:', modifiedSentence.decode("utf-8"))
# clientSocket.close()