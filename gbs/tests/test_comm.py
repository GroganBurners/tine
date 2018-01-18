from django.test import TestCase
import responses
from datetime import date
from gbs.models import Customer, Invoice
from gbs.comm import sms
from gbs.comm import email


class SMSTest(TestCase):
    def setUp(self):
        responses.add(responses.POST, sms.API_ENDPOINT,
                      json={'success': True}, status=200)

    @responses.activate
    def test_sms_send(self):
        response = sms.send_sms("Hello, World!", "+353890000000")
        self.assertEqual(response['success'], True)


class EmailTest(TestCase):
    def setUp(self):
        cust = Customer.objects.create(
            name="Neil Grogan",
            email="neil@grogan.ie",
            phone_number="+353871234567",
            street="Ballyda",
            county="KK",
            eircode="R95 CX65",
            country="IE")
        self.invoice = Invoice.objects.create(
            customer=cust,
            date=date(2018, 1, 1),
            invoice_id='R11D23',
            invoiced=False,
            draft=False,
            paid_date=date(2018, 1, 1))

    def test_invoice_send(self):
        self.assertEqual(email.send_invoice(self.invoice), 1)
