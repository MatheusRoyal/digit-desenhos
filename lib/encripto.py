from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def gerar_keys(size):
    key = RSA.generate(size)
    return key, key.public_key()

def gerar_cifra(target_key):
    return PKCS1_OAEP.new(key=target_key)

def encriptar(cifra, msg, encoding="utf-8"):
    if not isinstance(msg, bytes):
        msg = msg.encode(encoding)
    return cifra.encrypt(msg)

def decriptar(cifra, msg, encoding="utf-8"):
    return cifra.decrypt(msg).decode(encoding)

def enviar_key(key, sock):
    print(len(str(key.export_key())))
    return sock.send(key.export_key())

def receber_key(sock, size=1024):
    key = sock.recv(size)
    return RSA.import_key(key)

def enviar_msg(cifra, msg, sock, encoding="utf-8"):
    msg = encriptar(cifra, msg, encoding)
    #print(len(msg))
    sock.send(msg)

def receber_msg(cifra, sock, size=1024, encoding="utf-8"):
    msg = sock.recv(size)
    print(len(msg))
    return decriptar(cifra, msg, encoding)
