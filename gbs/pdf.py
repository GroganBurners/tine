from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4

def export_invoice(buf, invoice):
    canvas = Canvas(buf, pagesize=A4)
    canvas.save()
