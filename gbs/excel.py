from .models import Invoice, Expense
from openpyxl import Workbook
from openpyxl.compat import range
from openpyxl.utils import get_column_letter


def export_finances(buf):
    wb = Workbook()
    ws = wb.active
    ws.title = "FinanceSheet2018"

    # Sheet header, first row
    row_num = 0

    ws.append(['Date', 'Details', 'Company', 'Money Out', 'Money In', 'VAT Due In', 'VAT Due Out', 'VAT Total', 'Total' ])

    for invoice in Invoice.objects.all().order_by('invoice_date'):
        items = invoice.items.all()
        row = [invoice.invoice_date, items[0].description, invoice.customer.name + ' ' +invoice.customer.street, '', invoice.total(), '', invoice.total_vat(), '']
        ws.append(row)

    wb.save(buf)
