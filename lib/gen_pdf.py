import io
from PyPDF2 import PdfFileReader, PdfFileWriter
import subprocess
# Import the reportlab library
from reportlab.pdfgen import canvas
# The size of the page supposedly A4
#from reportlab.lib.pagesizes import A4
#import reportlab.lib.pagesizes as pgsiz
from reportlab.lib.units import mm
# The color of the watermark
from reportlab.lib import colors

from datetime import datetime


pt_to_mm = 0.3527777778
#PAGESIZE = A4
FONTNAME = 'Helvetica-Bold'
FONTSIZE = 8
# using colors module
# COLOR = colors.lightgrey
# or simply RGB
# COLOR = (190, 190, 190)
COLOR = colors.red
# The position attributes of the watermark
#X = 300
#Y = -590
# The rotation angle in order to display the watermark diagonally if needed
ROTATION_ANGLE = 90

#user = "Matheus"

def create_watermark(wm_text: str, x: float, y: float):
    """
    Creates a watermark template.
    """
    # Generate the output to a memory buffer
    output_buffer = io.BytesIO()
    # Default Page Size = A4
    PAGESIZE = (x*mm, y*mm)
    c = canvas.Canvas(output_buffer, pagesize=PAGESIZE)
    # you can also add image instead of text
    # c.drawImage("logo.png", X, Y, 160, 160)
    # Set the size and type of the font
    c.setFont(FONTNAME, FONTSIZE)
    # Set the color
    if isinstance(COLOR, tuple):
        color = (c/255 for c in COLOR)
        c.setFillColorRGB(*color)
    else:
        c.setFillColor(COLOR)
    # Rotate according to the configured parameter
    c.rotate(ROTATION_ANGLE)
    #c.text_Anchor = middle
    # Position according to the configured parameter
    #X = PAGESIZE[0]/2
    #Y = -9*PAGESIZE[1]/10
    X = PAGESIZE[1]/2
    Y = -PAGESIZE[0]+5
    c.drawString(X, Y, wm_text)
    c.save()
    return output_buffer

def save_watermark(wm_buffer, output_file):
    """
    Saves the generated watermark template to disk
    """
    with open(output_file, mode='wb') as f:
        f.write(wm_buffer.getbuffer())
    f.close()
    return True

def watermark_pdf(input_file: str, user: str, output_file: str):
    """
    Adds watermark to a pdf file.
    """
    timestamp = datetime.now()
    str_time = datetime.strftime(timestamp, '%Y/%m/%d - %H:%M:%S')

    wm_text = "Impresso por: " + user +" - " + str_time
    pdf_reader = PdfFileReader(open(input_file, 'rb'), strict=False)
    dim = pdf_reader.getPage(0).mediaBox
    x = float(dim[2])*pt_to_mm
    y = float(dim[3])*pt_to_mm

    wm_buffer = create_watermark(wm_text, x, y)
    wm_reader = PdfFileReader(wm_buffer)
    pdf_writer = PdfFileWriter()
    out = open(output_file, mode='wb')
    try:
        page = pdf_reader.getPage(0)
        page.mergePage(wm_reader.getPage(0))
        pdf_writer.addPage(page)
        pdf_writer.write(out)
    except Exception as e:
        print("Exception = ", e)
        return False, None, None
    return True, pdf_reader, pdf_writer

#watermark_pdf('entrada.pdf', user, 'saida.pdf')

#pdf = create_watermark(wm_text)
#pdf = save_watermark(pdf, "Teste.pdf")
#watermark_pdf('Chapa 1.PDF', wm_text, 'C:\\Users\\engenharia3\\Desktop\\Chapas proteção\\')
