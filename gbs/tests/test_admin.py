from datetime import date
from io import BytesIO
from unittest.mock import patch
from zipfile import ZipFile

import PyPDF2
from django.contrib.admin.options import ModelAdmin
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.core import mail
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.test import TestCase
from django.urls import reverse
from openpyxl import load_workbook

from gbs.models import Customer, Invoice


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
        self.assertEqual(wb.sheetnames[0], "FinanceSheet2018")


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

        pdfReader = PyPDF2.PdfReader(BytesIO(response.content))

        self.assertEqual(len(pdfReader.pages), 1)
        pageObj = pdfReader.pages[0]
        self.assertIn(self.invoice.customer.name, pageObj.extract_text())

    def test_delete_invoice_admin(self):
        """
        Ensure DELETE on admin works.
        """
        delete_url = reverse("gbsadmin:gbs_invoice_delete", args=[self.invoice.id])
        self.assertTrue(delete_url.endswith("/delete/"))
        response = self.client.get(delete_url)
        self.assertIsInstance(response, TemplateResponse)
        self.assertEqual(response.status_code, 200)

    def test_bulk_pdf_export_contains_each_invoice(self):
        other = Invoice.objects.create(customer=self.invoice.customer)
        response = self.client.post(
            reverse("gbsadmin:gbs_invoice_changelist"),
            {
                "action": "print_invoices",
                "_selected_action": [self.invoice.pk, other.pk],
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/zip")
        with ZipFile(BytesIO(response.content)) as archive:
            self.assertEqual(
                set(archive.namelist()), {self.invoice.file_name(), other.file_name()}
            )
            for name in archive.namelist():
                self.assertTrue(archive.read(name).startswith(b"%PDF"))

    def test_email_invoice_action(self):
        response = self.client.get(
            reverse("gbsadmin:invoice-email", args=[self.invoice.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "../")
        self.assertIn(
            "Invoice Email Sent.",
            [str(message) for message in get_messages(response.wsgi_request)],
        )
        self.invoice.refresh_from_db()
        self.assertTrue(self.invoice.invoiced)
        self.assertEqual(len(mail.outbox), 1)

    def test_bulk_email_action(self):
        other = Invoice.objects.create(customer=self.invoice.customer)
        response = self.client.post(
            reverse("gbsadmin:gbs_invoice_changelist"),
            {
                "action": "email_invoices",
                "_selected_action": [self.invoice.pk, other.pk],
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 2)
        self.assertFalse(Invoice.objects.filter(invoiced=False).exists())

    def test_sms_action_reports_delivery_result(self):
        for success, expected in [
            (True, "Invoice SMS Sent."),
            (False, "SMS sending failed. Please check the logs and try later."),
        ]:
            with self.subTest(success=success):
                with patch(
                    "gbs.models.sms.send_sms", return_value={"success": success}
                ) as send:
                    response = self.client.get(
                        reverse("gbsadmin:invoice-sms", args=[self.invoice.pk])
                    )
                self.assertEqual(response.status_code, 302)
                send.assert_called_once()
                self.assertIn(
                    expected,
                    [str(message) for message in get_messages(response.wsgi_request)],
                )

    @patch("gbs.models.sms.send_sms")
    def test_sms_action_without_phone_shows_error(self, send):
        customer = self.invoice.customer
        customer.phone_number = ""
        customer.save()
        response = self.client.get(
            reverse("gbsadmin:invoice-sms", args=[self.invoice.pk])
        )
        send.assert_not_called()
        self.assertIn(
            "No phone number present for customer.",
            [str(message) for message in get_messages(response.wsgi_request)],
        )
