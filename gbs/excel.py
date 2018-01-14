from .models import Invoice, Expense
from openpyxl import Workbook
from openpyxl.compat import range
from openpyxl.utils import get_column_letter
from decimal import Decimal
from io import BytesIO
from itertools import chain
from operator import attrgetter
import logging

logger = logging.getLogger(__name__)

def export_finances():
    wb = Workbook()
    ws = wb.active
    ws.title = "FinanceSheet2018"

    # Sheet header, first row
    row_num = 0

    ws.append(['Date', 'Details', 'Company', 'Money Out', 'Money In', 'VAT Due In', 'VAT Due Out', 'VAT Total', 'Total' ])
    invoices = Invoice.objects.all()
    expenses = Expense.objects.all()
    logger.error(invoices)
    logger.error(expenses)
    result_list = sorted(list(chain(invoices, expenses)), key=attrgetter('date'))
    logger.error(result_list)

    total = Decimal(0)

    for res in result_list:
        items = res.items.all()
        if type(res) == Invoice:
            total = total + res.total()
            row = [res.date, items[0].description, 'Customer', '', res.total(), '', res.total_vat(), '', total]
        else:
            total = total - res.total()
            row = [res.date, items[0].description, 'SUPPLIER', res.total(), '', res.total_vat(), '', '', total]
        ws.append(row)

    buffer = BytesIO()
    wb.save(buffer)
    xls = buffer.getvalue()
    buffer.close()
    return xls
