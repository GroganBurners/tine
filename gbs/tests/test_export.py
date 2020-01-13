from django.test import TestCase
from gbs.models import (Customer, Expense, ExpenseType, ExpenseItem,
                        Invoice, InvoiceItem, Supplier)
from gbs.export import excel_export, pdf
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
        suppl = Supplier.objects.create(
            name="Heating Parts Ltd.",
            email="info@example.com",
            phone_number="+44871234567",
            street="1 Huddersfield",
            county="KK",
            eircode="BT1 XYZ",
            country="UK")
        exp_type = ExpenseType.objects.create(type='Parts')
        self.expense = Expense.objects.create(
            supplier=suppl, date=date(
                2018, 1, 1), type=exp_type, notes='Ferroli Part')
        ExpenseItem.objects.create(
            description="Boiler Parts",
            unit_price=Decimal(70.48),
            vat_rate=Decimal(9.5),
            quantity=Decimal(1.00),
            expense=self.expense)

    def test_export_xls_correctly(self):
        result = excel_export.export_finances()
        self.assertIsInstance(result, bytes)
        wb = load_workbook(BytesIO(result))
        self.assertEqual(wb.get_sheet_names()[0], "FinanceSheet2018")

    def tearDown(self):
        Customer.objects.all().delete()
        Invoice.objects.all().delete()
        InvoiceItem.objects.all().delete()
        Supplier.objects.all().delete()
        Expense.objects.all().delete()
        ExpenseItem.objects.all().delete()


class PDFExportTest(TestCase):
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
        suppl = Supplier.objects.create(
            name="Heating Parts Ltd.",
            email="info@example.com",
            phone_number="+44871234567",
            street="1 Huddersfield",
            county="KK",
            eircode="BT1 XYZ",
            country="UK")
        exp_type = ExpenseType.objects.create(type='Parts')
        self.expense = Expense.objects.create(
            supplier=suppl, date=date(
                2018, 1, 1), type=exp_type, notes='Ferroli Part')
        ExpenseItem.objects.create(
            description="Boiler Parts",
            unit_price=Decimal(70.48),
            vat_rate=Decimal(9.5),
            quantity=Decimal(1.00),
            expense=self.expense)

    def test_export_pdf_correctly(self):
        invoice = Invoice.objects.get(invoice_id="R11D23")
        result = pdf.export_invoice(invoice)
        self.assertIsInstance(result, bytes)
        # Verify more info about PDF

    def tearDown(self):
        Customer.objects.all().delete()
        Invoice.objects.all().delete()
        InvoiceItem.objects.all().delete()
        Supplier.objects.all().delete()
        Expense.objects.all().delete()
        ExpenseItem.objects.all().delete()
