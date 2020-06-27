from datetime import date
from io import BytesIO

import django.urls
import PyPDF2
from django.contrib.admin.options import ModelAdmin
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.test import TestCase
from django.urls import reverse
from gbs.models import Customer, Invoice
from openpyxl import load_workbook


class MockRequest:
    pass


class MockSuperUser:
    def has_perm(self, perm):
        return True


request = MockRequest()
request.user = MockSuperUser()


class GBSAdminTests(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username="super", password="secret", email="super@example.com"
        )
        self.client.force_login(self.superuser)

    def test_export_xls_finances_admin(self):
        xls_url = reverse("gbsadmin:export-finances")
        self.assertTrue(xls_url.endswith("/xls/"))
        response = self.client.get(xls_url)
        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response["Content-Type"],
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        self.assertIsInstance(response.content, bytes)

        wb = load_workbook(BytesIO(response.content))
        self.assertEqual(wb.get_sheet_names()[0], "FinanceSheet2018")


class InvoiceAdminTests(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username="super", password="secret", email="super@example.com"
        )
        self.client.force_login(self.superuser)
        customer = Customer.objects.create(name="Neil Grogan", street="Ballyda")
        self.invoice = Invoice.objects.create(
            date=date(2018, 8, 1),
            customer=customer,
            invoice_id="130DFC",
            invoiced=False,
            draft=False,
            paid_date=date(2018, 9, 1),
        )
        self.site = AdminSite()

    def test_default_fields(self):
        ma = ModelAdmin(Invoice, self.site)
        self.assertEqual(
            list(ma.get_form(request).base_fields),
            ["date", "customer", "invoiced", "draft", "cash", "paid_date"],
        )
        self.assertEqual(
            list(ma.get_fields(request)),
            ["date", "customer", "invoiced", "draft", "cash", "paid_date"],
        )
        self.assertEqual(
            list(ma.get_fields(request, self.invoice)),
            ["date", "customer", "invoiced", "draft", "cash", "paid_date"],
        )
        self.assertIsNone(ma.get_exclude(request, self.invoice))

    def test_add_invoice_admin(self):
        """
        Ensure GET on the add_view works.
        """
        add_url = reverse("gbsadmin:gbs_invoice_add")
        self.assertTrue(add_url.endswith("/add/"))
        response = self.client.get(add_url)
        self.assertIsInstance(response, TemplateResponse)
        self.assertEqual(response.status_code, 200)

    def test_post_invoice_admin(self):
        pass
        # TODO
        # data = {}
        # add_url = reverse('gbsadmin:gbs_invoice_add')
        # self.assertTrue(add_url.endswith('/add/'))
        # response = self.post(add_url, data, follow=True)
        # self.assertEqual(response.status_code, 200)

    def test_changelist_invoice_admin(self):
        """
        Ensure CHANGELIST on admin works.
        """
        change_list_url = reverse("gbsadmin:gbs_invoice_changelist")
        self.assertTrue(change_list_url.endswith("/invoice/"))
        response = self.client.get(change_list_url)
        self.assertIsInstance(response, TemplateResponse)
        self.assertEqual(response.status_code, 200)

    def test_change_invoice_admin(self):
        """
        Ensure CHANGE on admin works.
        """
        change_url = reverse("gbsadmin:gbs_invoice_change", args=[self.invoice.id])
        self.assertTrue(change_url.endswith("/change/"))
        response = self.client.get(change_url)
        self.assertIsInstance(response, TemplateResponse)
        self.assertEqual(response.status_code, 200)

    def test_history_invoice_admin(self):
        """
        Ensure HISTORY on admin works.
        """
        history_url = reverse("gbsadmin:gbs_invoice_history", args=[self.invoice.id])
        self.assertTrue(history_url.endswith("/history/"))
        response = self.client.get(history_url)
        self.assertIsInstance(response, TemplateResponse)
        self.assertEqual(response.status_code, 200)

    def test_get_pdf_invoice_admin(self):
        """
        Ensure GET on the add_view works.
        """
        pdf_url = reverse("gbsadmin:invoice-pdf", args=[self.invoice.id])
        self.assertTrue(pdf_url.endswith("/pdf/"))
        response = self.client.get(pdf_url)
        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")
        self.assertIsInstance(response.content, bytes)

        pdfReader = PyPDF2.PdfFileReader(BytesIO(response.content))

        self.assertEqual(pdfReader.numPages, 1)
        pageObj = pdfReader.getPage(0)
        self.assertTrue(pageObj.extractText().find(self.invoice.customer.name))

    def test_delete_invoice_admin(self):
        """
        Ensure DELETE on admin works.
        """
        delete_url = reverse("gbsadmin:gbs_invoice_delete", args=[self.invoice.id])
        self.assertTrue(delete_url.endswith("/delete/"))
        response = self.client.get(delete_url)
        self.assertIsInstance(response, TemplateResponse)
        self.assertEqual(response.status_code, 200)
