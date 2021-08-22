import socket
import hashlib
from .criptografia import Criptografia
from .numeroPrimo import GeradorNumeroPrimo
from .gerarChaves import Chaves
from Crypto.Cipher import AES #biblioteca PyCryptodome

##Hash
class Resumo:
    def resumir(mensagem):
        m = bytes(mensagem,"utf-8")
        s = hashlib.sha256()
        s.update(m)
        return s.digest()
##Ks
# Chave simétrica
class CSimetrica:
    def encrypt(key, data):
        if len(key) % 16 != 0:
            key += ' ' * (16 - len(key)%16)
        if len(data) % 16 != 0:
            data += ' ' * (16 - len(data)%16)
        cipher = AES.new(bytes(key,"utf-8"), AES.MODE_ECB)
        ciphertext = cipher.encrypt(bytes(data,"utf-8"))
        return ciphertext

    def decrypt(key, ciphertext):
        print('tipo da key:',type(key))
        if len(key) % 16 != 0:
            key += ' ' * (16 - len(key)%16)
        if len(ciphertext) % 16 != 0:
            ciphertext += ' ' * (16 - len(ciphertext)%16)
        cipher = AES.new(bytes(key,"utf-8"), AES.MODE_ECB)
        msg = cipher.decrypt(ciphertext)
        return msg.decode("utf-8")
##K+/K-
class CAssimetrica:
    def gerarChaves():
        '''
        Gera a chave pública, privada, n é o produto de primos
        '''
        p = GeradorNumeroPrimo()
        numero_p = p.numero_primo
        q = GeradorNumeroPrimo()
        numero_q = q.numero_primo
        chaves = Chaves(numero_p,numero_q)
        KPP = chaves.gerar_chaves() #KPP[0] - chave pública/KPP[1] - chave privada
        n = numero_q*numero_p
        return (KPP[0],KPP[1],n,chaves)

    def cifrar(mensagem,e,n,chaves):
        '''
        O 'e' é a chave pública da outra parte
        o n eu pego de cima
        '''
        mensagem_cifrada = chaves.encripta_mensagem(mensagem,e,n)
        return mensagem_cifrada
    
    def decifrar(mensagem_cifrada,d,n,chaves): #O outro tem que mandar uma chave pública e um n
        '''
        d é a chave privada do outro cara

        '''
        mensagem = chaves.decripta_mensagem(mensagem_cifrada,d,n)
        return mensagem
##Conexão
class Conexao:
    def conectar(modo):
        if(modo==1):#cliente
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientSocket.connect((socket.gethostname(),5100))
            # quadrupla = CAssimetrica.gerarChaves()
            # return (quadrupla[0],quadrupla[1],quadrupla[2],quadrupla[3],clientSocket)
            return clientSocket
        else:#servidor
            serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            serverSocket.bind((socket.gethostname(),5100))
            print(socket.gethostname())
            serverSocket.listen(1)
            return serverSocket
    
    def desconectar(modo, s):
        if(modo==1):
            s.close()
        else:
            s.close()
## Envio
class Envio:
    def enviar(clientSocket,mensagem,chave_simetrica,e,d,n,chaves):
        clientSocket.send(bytes(CAssimetrica.cifrar((str(Resumo.resumir(mensagem))),d,n,chaves),"utf-8"))
        clientSocket.send(CSimetrica.encrypt(mensagem,chave_simetrica))
        clientSocket.send(bytes(CAssimetrica.cifrar((chave_simetrica),e,n,chaves),"utf-8"))
    
    def receber(clientSocket,e,d,n,chaves):
        resumo_cifrado = clientSocket.recv(1024)
        mensagem_cifrada = clientSocket.recv(1024)
        chave_cifrada = clientSocket.recv(1024)
        chave_simetrica = CAssimetrica.decifrar(chave_cifrada.decode("utf-8"),d,n,chaves)
        print('chave simetrica:', chave_simetrica)
        print('chave cifrada:', chave_cifrada)
        print('mensagem cifrada:', mensagem_cifrada)
        print('mensagem cifrada:', resumo_cifrado)
        # print('chave cifrada:', chave_cifrada)
        mensagem = CSimetrica.decrypt(chave_simetrica, mensagem_cifrada)
        resumo = CAssimetrica.decifrar(resumo_cifrado.decode("utf-8"),e,n,chaves)
        m = ''
        for i in range(0,8):
            m+=mensagem[i]
        resumo_m = str(Resumo.resumir(m))
        if(resumo_m==resumo):   
            return mensagem
        else:
            return 'Falha de autenticacao'