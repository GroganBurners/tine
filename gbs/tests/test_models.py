from decimal import Decimal
from datetime import date
from django.test import TestCase
from gbs.models import Customer, Invoice, InvoiceItem, Price

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

class InvoiceTest(TestCase):
    def setUp(self):
        cust = Customer.objects.create(name="Neil Grogan", email="neil@grogan.ie",
                                phone_number="+353871234567", street="Ballyda",
                                county="KK", eircode="R95 CX65",
                                country="IE")
        self.invoice = Invoice.objects.create(customer=cust, date=date(2018,1,1),
                invoice_id='R11D23', invoiced=False, draft=False,
                paid_date=date(2018,1,1))
        InvoiceItem.objects.create(description="Service", unit_price=Decimal(70.48),
                vat_rate=Decimal(13.5), quantity=Decimal(1.00), invoice=self.invoice)
                                              
    def test_invoice_values_set_correctly(self):
        invoice = Invoice.objects.get(invoice_id="R11D23")
        self.assertEqual(invoice.date, date(2018,1,1))
        self.assertEqual(invoice.invoice_id, 'R11D23')
        self.assertFalse(invoice.invoiced)
        self.assertFalse(invoice.draft)
        self.assertEqual(invoice.paid_date, date(2018,1,1))

        item = invoice.items.all()[0]
        self.assertEqual(item.description, "Service")
        # self.assertEqual(item.unit_price, Decimal(70.48))
        self.assertEqual(item.vat_rate, Decimal(13.5))
        self.assertEqual(item.quantity, Decimal(1.00))

        # self.assertEqual(item.total_amount(), "€ 80")


    def tearDown(self):
        Customer.objects.all().delete()
        Invoice.objects.all().delete()
        InvoiceItem.objects.all().delete()

class PriceTest(TestCase):
    def setUp(self):
        Price.objects.create(type="gas_service", cost=0.00, summer_offer=True)
        Price.objects.create(type="oil_service", cost=20.00, summer_offer=False)

    def test_gas_service_values_set_correctly(self):
        gas_price = Price.objects.get(type="gas_service")
        self.assertEqual(gas_price.cost, 0.00)
        self.assertTrue(gas_price.summer_offer)

    def test_oil_service_values_set_correctly(self):
        oil_price = Price.objects.get(type="oil_service")
        self.assertEqual(oil_price.cost, 20.00)
        self.assertFalse(oil_price.summer_offer)
