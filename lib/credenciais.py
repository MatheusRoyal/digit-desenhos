from dotenv import dotenv_values
import os
import base64, hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

def carregar_usuarios():

    senha = input('Senha mestre - ')

    usuarios = dotenv_values('C:\\Users\\engenharia3\\Desktop\\Projetos Python\\digit-desenhos\\credenciais.env')

    f = gerar_key(senha)
    for entry in usuarios:
        value = usuarios[entry]
        value = f.decrypt(value.encode('ascii'))
        usuarios[entry] = value.decode()
    return usuarios

def gerar_key(key):

    backend = default_backend()
    # salt = os.urandom(16)
    salt = b'thisissomething'

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=backend
    )

    key = base64.urlsafe_b64encode(kdf.derive(key.encode()))

    return Fernet(key)

def cadastrar_usuario():
    senha = input('Senha mestre - ')
    usuario_cad = input('Usuário novo - ')
    senha_cad = input('Senha nova - ')

    f = gerar_key(senha)

    usuario_cad = usuario_cad.upper()

    senha_cad = f.encrypt(senha_cad.encode('ascii'))

    environ = open('credenciais.env', 'a')
    environ.write(usuario_cad+"="+senha_cad.decode()+'\n')
