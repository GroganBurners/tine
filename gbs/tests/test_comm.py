from datetime import date
from unittest.mock import patch

import responses
from django.test import TestCase
from requests.exceptions import Timeout

from gbs.comm import email, sms
from gbs.models import Customer, Invoice


class SMSTest(TestCase):
    def setUp(self):
        responses.add(
            responses.POST, sms.API_ENDPOINT, json={"success": True}, status=200
        )

    @responses.activate
    def test_sms_send(self):
        response = sms.send_sms("+353890000000", "Hello, World!")
        self.assertEqual(response["success"], True)

    @patch("gbs.comm.sms.requests.post", side_effect=Timeout("SMS service timed out"))
    def test_sms_request_has_timeout_and_propagates_failure(self, post):
        with self.assertRaises(Timeout):
            sms.send_sms("+353890000000", "Hello, World!")
        post.assert_called_once()
        self.assertEqual(post.call_args.kwargs["timeout"], 15)


class EmailTest(TestCase):
    def setUp(self):
        cust = Customer.objects.create(
            name="Neil Grogan",
            email="neil@grogan.ie",
            phone_number="+353871234567",
            street="Ballyda",
            county="KK",
            eircode="R95 CX65",
            country="IE",
        )
        self.invoice = Invoice.objects.create(
            customer=cust,
            date=date(2018, 1, 1),
            invoice_id="R11D23",
            invoiced=False,
            draft=False,
            paid_date=date(2018, 1, 1),
        )

    def test_invoice_send(self):
        self.assertEqual(email.send_invoice(self.invoice), 1)
