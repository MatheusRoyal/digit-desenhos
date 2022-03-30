import os
import subprocess

def identificar(num):
    partes = num.split(".")
    if partes[0] == "00":
        maq = partes[0] + "." + partes[1]
        path = achar_gabarito(maq, num)
    else:
        setorial = partes[0]
        maq = setorial[len(setorial)-3:]
        setor = setorial.replace(maq, "")
        if len(setor) == 1:
            setor = "0" + setor
        if setor == "16":
            path = achar_gabarito(setor + maq, num)
        else:
            path = achar_ferramenta(maq, setor, num)
    return path


def achar_ferramenta(maq, setor, num):
    path = "N:\\Engenharia\\Desenhos\\Ferramentas\\"
    for line in os.listdir(path):
        setor_busca = line.split()[1]
        if setor_busca == setor:
            path = path + line + "\\"
            break

    for line in os.listdir(path):
        maq_busca = line.split("-")[0]
        maq_busca = maq_busca.strip()
        if maq_busca[len(maq_busca)-3:] == maq:
            path = path + line + "\\"
            break
    return achar_pdf(path, num)

def achar_gabarito(gab, num):
    path = "N:\\Engenharia\\Desenhos\\Gabaritos\\"
    print("1 - " + path)
    path = path + gab + "\\"
    print("2 - " + path)
    return achar_pdf(path, num)

def achar_pdf(path, num):
    try:
        for file in os.listdir(path):
            fileparts = file.split('.')
            filename = ''.join(part + '.' for part in fileparts[:-1])
            filename = filename[:-1]
            try:
                filename, version = filename.split('-')
            except:
                version = ''
            if (file.endswith(".pdf") or file.endswith(".PDF")) and file.startswith(num):
                path = path + file
                break
    except:
        print("Pdf não encontrado")
    return path
