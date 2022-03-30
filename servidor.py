import socket
import os
import time
from multiprocessing import Process
import lib.credenciais as credenciais
import lib.encripto as crip
import lib.setores as setores
import lib.gen_pdf as gen_pdf


def handle_client(conn, addr, usuarios):
    print(addr, 'aceito')
    priv_key_log, pub_key_log = crip.gerar_keys(1024)
    crip.enviar_key(pub_key_log, conn)
    decipher = crip.gerar_cifra(priv_key_log)
    user = conn.recv(1024)
    user = crip.decriptar(decipher, user)
    user = user.upper()
    print(user)
    pword = conn.recv(1024)
    pword = crip.decriptar(decipher, pword)
    print(pword)
    if user in usuarios and usuarios[user] == pword:
        conn.sendall(b'Aceito')
        print('Aceito')
    else:
        conn.sendall(b'Rejeitado')
        print('Usuario não autenticado')
        s.close()
        return
    flag = True
    transaction = "N:\\Publico\\Manutenção\\Temp\\"
    while flag:
        while True:
            recebido = conn.recv(1024)
            if recebido:
                break
        cod = crip.decriptar(decipher, recebido)
        print(cod)
        try:
            fpath = setores.identificar(cod)
            print(fpath)
            cod = fpath.split('\\')[-1]
            gen_pdf.watermark_pdf(fpath, user, transaction+cod)
            conn.sendall(cod.encode())
            flag = False
        except:
            conn.sendall(b'nada')
            print("não foi possivel enviar o caminho do pdf")
    #conn.send(fpath.encode())
    print("Copied")
    time.sleep(10)
    print("Waited")
    filename = fpath.split('\\')
    filename = str(filename[-1])
    print(transaction + filename)
    os.remove(transaction + '\\' + filename)
    print("Deleted")
    return

if __name__ == '__main__':
    usuarios = credenciais.carregar_usuarios()
    print(usuarios)

    #Definir local do servidor

    HOST = '192.168.254.71' #176  # Standard loopback interface address (localhost)
    PORT = 65450        # Port to listen on (non-privileged ports are > 1023)
    #context = ssl.create_default_context()

    #context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    #context.load_verify_locations('C:\\Program Files\\Git\\usr\\bin\\privkey.pem')

    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            conn, addr = s.accept()
            arguments = (conn, addr, usuarios)
            p = Process(target = handle_client, args = arguments)
            p.start()
