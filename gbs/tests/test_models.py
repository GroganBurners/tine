from django.test import TestCase
from gbs.models import Customer

class CustomerTest(TestCase):
    def setUp(self):
        Customer.objects.create(name="Neil Grogan", email="neil@grogan.ie",
                                phone_number="+353871234567", street="Ballyda",
                                county="KK", eircode="R95 CX65",
                                country="IE")
    def test_customer_values_set_correctly(self):
        cust = Customer.objects.get(name="Neil Grogan")
        self.assertEqual(cust.email, "neil@grogan.ie")
        self.assertEqual(cust.phone_number, "+353871234567")
        self.assertEqual(cust.street, "Ballyda")
        self.assertEqual(cust.county, "KK")
        self.assertEqual(cust.eircode, "R95 CX65")
        self.assertEqual(cust.country, "IE")

    def tearDown(self):
        Customer.objects.all().delete()
