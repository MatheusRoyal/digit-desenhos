import os
import subprocess
import api_solidworks as sw

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
    #try:
    version = -1
    file_list = os.listdir(path)
    for temp_file in file_list:
        if not (temp_file.startswith(num) and (temp_file.endswith(".SLDDRW") or (temp_file.endswith(".pdf") or temp_file.endswith(".PDF")))):
            continue
        fileparts = temp_file.split('.')
        temp_filename = ''.join(part + '.' for part in fileparts[:-1])
        temp_filename = temp_filename[:-1]
        try:
            temp_version = temp_filename.split('-')[1]
        except:
            temp_version = "00"
        if int(temp_version) > int(version):
            filename = temp_filename
            version = temp_version
            file = temp_file
            print(filename, version, file)
    if (filename + ".pdf" in file_list):
        path = path + filename + ".pdf"
    elif (filename + ".PDF" in file_list):
        path = path + filename + ".PDF"
    elif (filename + ".SLDDRW" in file_list):
        sw.gerar_pdf(path, filename + ".SLDDRW")
        path = path + filename + ".pdf"

    print(path)
        #try:
        #    filename, version = filename.split('-')
        #except:
        #    version = ''
        #if file.endswith(".pdf") or file.endswith(".PDF"):
        #    path = path + file
        #    break
    #except:
    print("Pdf não encontrado")
    return path

if __name__ == "__main__":
    num = "33149.031"
    identificar(num)
