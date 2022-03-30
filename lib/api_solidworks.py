import pySW

def gerar_pdf(path, file):
    sw = pySW.commSW()
    sw.connectToSW()
    sw.openDrw(path + "\\" + file)
    sw.save(path, file.replace(".SLDDRW", ""), 'pdf')
