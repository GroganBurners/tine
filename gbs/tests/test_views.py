import unittest
from django.test import Client
from gbs.models import Price


class ViewsTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_homepage(self):
        # Issue a GET request.
        price = Price(type="repair_call_out", cost=80.00, summer_offer=False)
        price.save()
        response = self.client.get('/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            str(response.context['repair_fees'][0]), "Repair Call Out Fee (First Hour) €80")

