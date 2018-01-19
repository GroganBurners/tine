from django.test import TestCase
from gbs.models import Customer, Invoice, InvoiceItem
from gbs.export import excel_export
from openpyxl import load_workbook
from datetime import date
from decimal import Decimal
from io import BytesIO


class XLSExportTest(TestCase):
    def setUp(self):
        cust = Customer.objects.create(
            name="Neil Grogan", email="neil@grogan.ie",
            phone_number="+353871234567", street="Ballyda",
            county="KK", eircode="R95 CX65", country="IE")
        self.invoice = Invoice.objects.create(
            customer=cust,
            date=date(2018, 1, 1), invoice_id='R11D23',
            invoiced=False, draft=False,
            paid_date=date(2018, 1, 1))
        InvoiceItem.objects.create(
            description="Service",
            unit_price=Decimal(70.48),
            vat_rate=Decimal(13.5),
            quantity=Decimal(1.00),
            invoice=self.invoice)

    def test_export_xls_correctly(self):
        result = excel_export.export_finances()
        self.assertIsInstance(result, bytes)
        wb = load_workbook(BytesIO(result))
        self.assertEqual(wb.get_sheet_names()[0], "FinanceSheet2018")
