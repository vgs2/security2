#!/usr/bin/env python3

import socket               # Import socket module
import _thread as thread
import pickle
import os

ELEICAO_PATH = 'eleicao.p'
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

help = b'Segue abaixo uma lista dos comandos disponiveis\n1 - resultados - Exibe o resultado de todas as eleicoes.\n2 - criarsessao <nome> <opcao1> <opcao2> ...  <opcaon>  - Cria uma nova sessao de votacao com as opcoes passadas\n3 - votar <eleicao> <candidato> - Um comando com multiplas funcionalidades. Use sem argumentos para exibir as sessoes disponiveis para votacao\nUse apenas com o argumento <eleicao> para exibir os candidatos disponiveis nesta sessao. E por fim utilize em conjunto com os dois argumentos para votar'


def criarsessao(mensagem, eleicoes):
    separate = mensagem.split(' ')
    # checar quantidade minima de argumentos
    if (len(separate) < 4):
        return 'Menos de 3 argumentos foram recebidos, por favor refaca a operacao'
    elif (len(separate) > 7):
        return 'Mais de 7 argumentos foram recebidos, por favor refaca a operacao'
    else:
        escolhas = []
        nome_escolhas = []
        for aux in separate[2:]:
            nome_escolhas.append(aux)
        escolhas = [{'id':a, 'nome':nome_escolhas[a], 'votos':[]} for a in range(len(nome_escolhas))]
        if(len(eleicoes==0)):
            eleicoes.append({'nome':separate[1],'escolhas':escolhas})
        else:
            def check_name(name, list_dict):
                for a in list_dict:
                    if a['nome'] == name:
                        return 0
                return 1
            # se nao for vazio, checa se ja tem alguma sessao com o mesmo nome
            nome = separate[1]
            if not check_name(nome, eleicoes):
                return 'O nome desta sessao ja existe, tente novamente'
            else:
                eleicoes.append({'nome':separate[1],'escolhas':escolhas})
                return 'Sessao criada com sucesso.'






    



def on_new_client(conn,addr):
    while True:
        data = conn.recv(1024).decode()
        if (data == 'help'):
            conn.send(help)
        elif (repr(data) == 'resultados'):
            conn.send(b'resultados')
        elif (repr(data).split(' ')[0] == 'criarsessao'):
            
        # elif (repr(data) == b'help'):
        if (data == b'Hello, world'):
            print('ok!')
        if not data:
            break
    conn.close()

if (os.path.isfile(ELEICAO_PATH)):
    with open('data.p', 'rb') as fp:
        eleicoes = pickle.load(fp)
else: eleicoes = []


s = socket.socket()         # Create a socket object

print ('Server started!')
print ('Waiting for clients...')

s.bind((HOST, PORT))        # Bind to the port
s.listen()                 # Now wait for client connection.

while True:
   c, addr = s.accept()     # Establish connection with client.
   thread.start_new_thread(on_new_client,(c,addr))
s.close()