import socket
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import hashlib
import base64

def encrypt_with_symmetric(message, fernet_key):
    fernet = Fernet(fernet_key)
    return fernet.encrypt(message)

def decrypt_with_symmetric(encrypted_message, fernet_key):
    fernet = Fernet(fernet_key)
    return fernet.decrypt(encrypted_message)

def encrypt_with_publickey(message, public_key_path):
    with open(public_key_path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
    encrypted = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
        )
    return encrypted

def decrypt_with_privatekey(encrypted_message, private_key_path):
    with open(private_key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    original_message = private_key.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
            )
        )
    return original_message

def sign_with_privatekey(message, private_key_path):
    '''
    Recebe uma mensagem em formato de bytes e o caminho da private key
    que será usada para assinar a mensagem
    retorna a assinatura
    '''
    with open(private_key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    signature = private_key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
    return signature

def check_signature(signature, message, public_key_path):
    with open(public_key_path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
    try: 
        public_key.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        verification = True
    except: verification = False
    return verification

def resumir(mensagem):
    m = bytes(mensagem,"utf-8")
    s = hashlib.sha256()
    s.update(m)
    return s.digest()

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            # encoded_message = conn.recv(1024)
            encrypted_message = conn.recv(1024)
            # encrypted_message = base64.b64decode(encoded_message)
            decoded_message = base64.b64decode(encrypted_message)
            message = decrypt_with_privatekey(encrypted_message,'private_key_server.pem')
            print(message)
            # data = conn.recv(1024)
            # print(2)
            # data = conn.recv(1024)
            # print(3)
            if not encrypted_message:
                break
            conn.sendall(b'ok')