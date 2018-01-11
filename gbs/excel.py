from .models import Invoice, Expense
from openpyxl import Workbook
from openpyxl.compat import range
from openpyxl.utils import get_column_letter


def export_finances():
    wb = Workbook()
    ws = wb.active
    ws.title = "FinanceSheet2017"

    # Sheet header, first row
    row_num = 0

    ws.append(['Date', 'Details', 'Company', 'Money Out', 'Money In', 'VAT Due In', 'VAT Due Out', 'VAT Total', 'Total' ])


    rows = Invoice.objects.all().values_list('invoice_date', 'customer__name', 'customer__address', 'total')
    for row in rows:
        ws.append(row)

    wb.save()
