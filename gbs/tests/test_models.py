from decimal import Decimal
from datetime import date
from django.test import TestCase
from gbs.models import (Customer, Expense, ExpenseItem, ExpenseType,
                        HeroImage, Invoice, InvoiceItem, Price, Supplier)


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


class SupplierTest(TestCase):

    def setUp(self):
        Supplier.objects.create(
            name="Heating Parts Ltd.",
            email="info@example.com",
            phone_number="+44871234567",
            street="1 Huddersfield",
            county="KK",
            eircode="BT1 XYZ",
            country="UK")

    def test_supplier_values_set_correctly(self):
        suppl = Supplier.objects.get(name="Heating Parts Ltd.")
        self.assertEqual(suppl.email, "info@example.com")
        self.assertEqual(suppl.phone_number, "+44871234567")
        self.assertEqual(suppl.street, "1 Huddersfield")
        self.assertEqual(suppl.county, "KK")
        self.assertEqual(suppl.eircode, "BT1 XYZ")
        self.assertEqual(suppl.country, "UK")

    def tearDown(self):
        Supplier.objects.all().delete()


class InvoiceTest(TestCase):
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
            date=date(
                2018,
                1,
                1),
            invoice_id='R11D23',
            invoiced=False,
            draft=False,
            paid_date=date(
                2018,
                1,
                1))
        InvoiceItem.objects.create(
            description="Service",
            unit_price=Decimal(70.48),
            vat_rate=Decimal(13.5),
            quantity=Decimal(1.00),
            invoice=self.invoice)

    def test_invoice_values_set_correctly(self):
        invoice = Invoice.objects.get(invoice_id="R11D23")
        self.assertEqual(invoice.date, date(2018, 1, 1))
        self.assertEqual(invoice.invoice_id, 'R11D23')
        self.assertFalse(invoice.invoiced)
        self.assertFalse(invoice.draft)
        self.assertEqual(invoice.paid_date, date(2018, 1, 1))

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


class ExpenseTest(TestCase):
    def setUp(self):
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

    def test_expense_values_set_correctly(self):
        expense = Expense.objects.get(notes='Ferroli Part')
        supp = Supplier.objects.get(name="Heating Parts Ltd.")
        e_type = ExpenseType.objects.get(type='Parts')
        self.assertEqual(expense.supplier, supp)
        self.assertEqual(expense.date, date(2018, 1, 1))
        self.assertEqual(expense.type, e_type)
        self.assertEqual(expense.notes, "Ferroli Part")
        item = expense.items.all()[0]
        self.assertEqual(item.description, "Boiler Parts")
        # self.assertEqual(item.unit_price, Decimal(70.48))
        self.assertEqual(item.vat_rate, Decimal(9.5))
        self.assertEqual(item.quantity, Decimal(1.00))

        # self.assertEqual(item.total_amount(), "€ 80")

    def tearDown(self):
        Supplier.objects.all().delete()
        Expense.objects.all().delete()
        ExpenseItem.objects.all().delete()


class PriceTest(TestCase):
    def setUp(self):
        Price.objects.create(type="gas_service", cost=0.00, summer_offer=True)
        Price.objects.create(
            type="oil_service",
            cost=20.00,
            summer_offer=False)

    def test_gas_service_values_set_correctly(self):
        gas_price = Price.objects.get(type="gas_service")
        self.assertEqual(gas_price.cost, 0.00)
        self.assertTrue(gas_price.summer_offer)

    def test_oil_service_values_set_correctly(self):
        oil_price = Price.objects.get(type="oil_service")
        self.assertEqual(oil_price.cost, 20.00)
        self.assertFalse(oil_price.summer_offer)

    def tearDown(self):
        Price.objects.all().delete()


class HeroImageTest(TestCase):
    def setUp(self):
        HeroImage.objects.create(title="Gas Offers", image="/img/test.jpg",
                                 teaser_text="Buy Now!",
                                 active=True,
                                 use_button=False,
                                 button_text="Gas Offers",
                                 button_link="#gas")

    def test_hero_image_values_set_correctly(self):
        himg = HeroImage.objects.get(title="Gas Offers")
        self.assertEqual(himg.image, "/img/test.jpg")
        self.assertTrue(himg.active)
        self.assertFalse(himg.use_button)
        self.assertEqual(himg.teaser_text, "Buy Now!")
        self.assertEqual(himg.button_text, "Gas Offers")
        self.assertEqual(himg.button_link, "#gas")

    def tearDown(self):
        HeroImage.objects.all().delete()
