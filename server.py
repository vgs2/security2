from ZVprotect import ZVprotect as ZV
import pickle

N_SERVER_PATH = 'keys/n.key'
SERVER_PUBLIC_KEY_PATH = 'keys/server_public_key.key'
SERVER_PRIVATE_KEY_PATH = 'keys/server_private_key.key'

with open(SERVER_PUBLIC_KEY_PATH, 'rb') as fp:
    server_public_key = pickle.load(fp)
with open(SERVER_PRIVATE_KEY_PATH, 'rb') as fp:
    server_private_key = pickle.load(fp)
with open(N_SERVER_PATH, 'rb') as fp:
    n_server = pickle.load(fp)

serverSocket = ZV.Conexao.conectar(modo=0)

while 1:
    clientSocket, address = serverSocket.accept()
    client_public_key = clientSocket.recv(1024).decode('utf-8')
    n_client = clientSocket.recv(1024).decode()

    mensagem = ZV.Envio.receber(clientSocket, client_public_key, server_private_key, n_client, ZV.CAssimetrica.gerarChaves()[3])
    print(mensagem)


    # sentence = clientSocket.recv(1024)
    # print(sentence.decode())
    # capitalizedSentence = (sentence.decode("utf-8")).upper()
    # clientSocket.send(bytes(capitalizedSentence, "utf-8"))
    # clientSocket.close()