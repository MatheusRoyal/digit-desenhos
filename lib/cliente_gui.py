import socket
import subprocess
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import lib.encripto as crip

HOST = '192.168.254.71'  # Standard loopback interface address (localhost)
PORT = 65450        # Port to listen on (non-privileged ports are > 1023)


def connect_serv():
    # create an INET, STREAMing socket
    print("Hello")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Hello")

    s.connect((HOST, PORT))
    print("Hello")
    pub_key_log = crip.receber_key(s)
    print("Connected")
    cipher = crip.gerar_cifra(pub_key_log)
    return s, cipher

# user = input("Usuario - ")
# crip.enviar_msg(cipher, user, s)
# pword = input("Senha - ")
# crip.enviar_msg(cipher, pword, s)

def cred(cipher, user, pword, connection):
    crip.enviar_msg(cipher, user, connection)
    crip.enviar_msg(cipher, pword, connection)
    conf = connection.recv(1024)
    if conf != b'Aceito':
        return False
    return True

# conf = s.recv(1024)
# if conf != b'Aceito':
#     quit()

def get_pdf(cipher, cod, connection):
    print("Hello")
    crip.enviar_msg(cipher, cod, connection)
    print("Hello")
    res = connection.recv(1024)
    return res

    #temp = "\\\\192.168.254.246\\Dados\\Publico\\Manutenção\\Temp\\" + cod + ".pdf"
    #subprocess.Popen([temp], shell=True)

# cod = str(input("N° desenho - "))
# crip.enviar_msg(cipher, cod, s)

# temp = "\\\\192.168.254.246\\Dados\\Publico\\Manutenção\\Temp\\" + cod + ".pdf"
#temp = "N:\\Publico\\Manutenção\\Temp\\" + cod + ".pdf"

# s.recv(1024)
# subprocess.Popen([temp], shell=True)
