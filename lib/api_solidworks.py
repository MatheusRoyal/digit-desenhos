import pySW

def gerar_pdf(path, file):
    #pathIn = 'N:\\Engenharia\\Desenhos\\Ferramentas\\Setor 01 - Conformação\\1001 - Conformadora de Eixo'

    #partIn = '1001.015-07.SLDDRW'

    #pathOut = 'N:\\Publico\\Manutenção\\Temp'

    #partOut = '1001.015-07'

    sw = pySW.commSW()
    sw.connectToSW()
    sw.openDrw(path + "\\" + file)
    sw.save(path, file.replace(".SLDDRW", ""), 'pdf')
