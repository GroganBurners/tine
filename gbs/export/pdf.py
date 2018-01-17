from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Table
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from io import BytesIO
from gbs.conf import settings
import os


def draw_header(canvas):
    """ Draws the invoice header """
    canvas.setStrokeColorRGB(0.9, 0.5, 0.2)
    canvas.setFillColorRGB(0.2, 0.2, 0.2)
    canvas.setFont('Helvetica', 16)
    canvas.drawString(18 * cm, -1 * cm, 'Invoice')
    canvas.drawString(1 * cm, -1 * cm, 'Grogan Burner Services')
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, '../static/images/export/flames.png')
    canvas.drawInlineImage(filename, 7.1 * cm, -1.1 * cm, 24, 30)
    canvas.setLineWidth(4)
    canvas.line(0, -1.25 * cm, 21.7 * cm, -1.25 * cm)


def draw_address(canvas):
    """ Draws the business address """
    business_details = (
        u'GROGAN BURNER SERVICES LTD',
        u'BALLYDA',
        u'DANESFORT',
        U'KILKENNY',
        U'R95 CC92',
        U'IRELAND',
        u'',
        u'',
        u'Phone: ' + settings.PHONE,
        u'Email: ' + settings.EMAIL,
        u'Website: ' + settings.WEBSITE,
        u'Reg No: ' + settings.REG_NO,
        u'VAT No: ' + settings.VAT_NO
    )
    canvas.setFont('Helvetica', 9)
    textobject = canvas.beginText(13 * cm, -2.5 * cm)
    for line in business_details:
        textobject.textLine(line)
    canvas.drawText(textobject)


def draw_footer(canvas):
    """ Draws the invoice footer """
    note = (
        u'Bank Details: ' +
        settings.BANK_ADDRESS,
        u'Sort Code: ' +
        settings.SORT_CODE +
        ' BIC: ' +
        settings.BIC +
        ' IBAN: ' +
        settings.IBAN +
        ' (Quote invoice number).',
        u'Please pay via bank transfer or cheque. All payments should be made in EURO.',
        u'Make cheques payable to Grogan Burner Services Ltd.',
    )
    textobject = canvas.beginText(1 * cm, -27 * cm)
    for line in note:
        textobject.textLine(line)
    canvas.drawText(textobject)


def export_invoice(invoice):
    """ Draws the invoice """
    buffer = BytesIO()
    canvas = Canvas(buffer, pagesize=A4)
    canvas.translate(0, 29.7 * cm)
    canvas.setFont('Helvetica', 10)

    canvas.saveState()
    draw_header(canvas)
    canvas.restoreState()

    canvas.saveState()
    draw_footer(canvas)
    canvas.restoreState()

    canvas.saveState()
    draw_address(canvas)
    canvas.restoreState()

    # Client address
    textobject = canvas.beginText(1.5 * cm, -2.5 * cm)
    if invoice.customer.name:
        textobject.textLine(invoice.customer.name)
    if invoice.customer.street:
        textobject.textLine(invoice.customer.street)
    if invoice.customer.county:
        textobject.textLine(invoice.customer.county)
    if invoice.customer.eircode:
        textobject.textLine(invoice.customer.eircode)
    if invoice.customer.country:
        textobject.textLine(invoice.customer.country)
    canvas.drawText(textobject)

    # Info
    textobject = canvas.beginText(1.5 * cm, -6.75 * cm)
    textobject.textLine(u'Invoice Number: %s' % invoice.invoice_id)
    textobject.textLine(
        u'Invoice Date: %s' %
        invoice.date.strftime('%d %b %Y'))
    # textobject.textLine(u'Client: %s' % invoice.customer.name)
    canvas.drawText(textobject)

    # Items
    data = [[u'Description', 'Quantity', u'VAT Rate', u'Price', 'Amount'], ]
    for item in invoice.items.all():
        data.append([
            item.description,
            item.quantity_amount(),
            item.vat_rate_amount(),
            item.unit_price_amount(),
            item.total_ex_vat_amount(),
        ])
    data.append([u'', u'', u'', u'Subtotal:', invoice.total_ex_vat_amount()])
    data.append([u'', u'', u'', u'VAT Total:', invoice.total_vat_amount()])
    data.append([u'', u'', u'', u'Total:', invoice.total_amount()])
    table = Table(data, colWidths=[10 * cm, 2 * cm, 2 * cm, 2 * cm, 2.5 * cm])
    table.setStyle([
        ('FONT', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), (0.2, 0.2, 0.2)),
        ('GRID', (0, 0), (-1, -4), 1, (0.7, 0.7, 0.7)),
        ('GRID', (-2, -1), (-1, -1), 1, (0.7, 0.7, 0.7)),
        ('ALIGN', (-2, 0), (-1, -1), 'RIGHT'),
        ('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)),
    ])
    tw, th, = table.wrapOn(canvas, 15 * cm, 19 * cm)
    table.drawOn(canvas, 1 * cm, -8 * cm - th)

    canvas.showPage()
    buffer.name = invoice.file_name()
    canvas.save()
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
