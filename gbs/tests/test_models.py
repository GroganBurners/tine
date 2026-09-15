from datetime import date
from decimal import Decimal
from unittest.mock import patch

from django.core import mail
from django.test import TestCase

from gbs.models import (
    Customer,
    Expense,
    ExpenseItem,
    ExpenseType,
    HeroImage,
    Invoice,
    InvoiceItem,
    Price,
    Supplier,
)


class CustomerTest(TestCase):
    def setUp(self):
        Customer.objects.create(
            name="Neil Grogan",
            email="neil@grogan.ie",
            phone_number="+353871234567",
            street="Ballyda",
            county="KK",
            eircode="R95 CX65",
            country="IE",
        )

    def test_customer_values_set_correctly(self):
        cust = Customer.objects.get(name="Neil Grogan")
        self.assertEqual(cust.email, "neil@grogan.ie")
        self.assertEqual(cust.phone_number, "+353871234567")
        self.assertEqual(cust.street, "Ballyda")
        self.assertEqual(cust.county, "KK")
        self.assertEqual(cust.eircode, "R95 CX65")
        self.assertEqual(cust.country, "IE")

    def test_customer_str_value_set_correctly(self):
        cust = Customer.objects.get(name="Neil Grogan")
        self.assertEqual(cust.__str__(), "Neil Grogan (Ballyda)")

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
            country="UK",
        )

    def test_supplier_values_set_correctly(self):
        suppl = Supplier.objects.get(name="Heating Parts Ltd.")
        self.assertEqual(suppl.email, "info@example.com")
        self.assertEqual(suppl.phone_number, "+44871234567")
        self.assertEqual(suppl.street, "1 Huddersfield")
        self.assertEqual(suppl.county, "KK")
        self.assertEqual(suppl.eircode, "BT1 XYZ")
        self.assertEqual(suppl.country, "UK")

    def test_supplier_str_value_set_correctly(self):
        suppl = Supplier.objects.get(name="Heating Parts Ltd.")
        self.assertEqual(suppl.__str__(), "Heating Parts Ltd.")

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
        InvoiceItem.objects.create(
            description="Service",
            unit_price=Decimal(70.48),
            vat_rate=Decimal(13.5),
            quantity=Decimal(1.00),
            invoice=self.invoice,
        )

    def test_invoice_values_set_correctly(self):
        invoice = Invoice.objects.get(invoice_id="R11D23")
        self.assertEqual(invoice.date, date(2018, 1, 1))
        self.assertEqual(invoice.invoice_id, "R11D23")
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
            country="UK",
        )
        exp_type = ExpenseType.objects.create(type="Parts")
        self.expense = Expense.objects.create(
            supplier=suppl, date=date(2018, 1, 1), type=exp_type, notes="Ferroli Part"
        )
        ExpenseItem.objects.create(
            description="Boiler Parts",
            unit_price=Decimal(70.48),
            vat_rate=Decimal(9.5),
            quantity=Decimal(1.00),
            expense=self.expense,
        )

    def test_expense_values_set_correctly(self):
        expense = Expense.objects.get(notes="Ferroli Part")
        supp = Supplier.objects.get(name="Heating Parts Ltd.")
        e_type = ExpenseType.objects.get(type="Parts")
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

    def test_expense_type_str_value_set_correctly(self):
        e_type = ExpenseType.objects.get(type="Parts")
        self.assertEqual(e_type.__str__(), "Parts")

    def tearDown(self):
        Supplier.objects.all().delete()
        Expense.objects.all().delete()
        ExpenseItem.objects.all().delete()


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

    def test_oil_service_str_value_set_correctly(self):
        oil_price = Price.objects.get(type="oil_service")
        self.assertEqual(oil_price.__str__(), "Oil Service €20")

    def tearDown(self):
        Price.objects.all().delete()


class HeroImageTest(TestCase):
    def setUp(self):
        HeroImage.objects.create(
            title="Gas Offers",
            image="/img/test.jpg",
            teaser_text="Buy Now!",
            active=True,
            use_button=False,
            button_text="Gas Offers",
            button_link="#gas",
        )

    def test_hero_image_values_set_correctly(self):
        himg = HeroImage.objects.get(title="Gas Offers")
        self.assertEqual(himg.image, "/img/test.jpg")
        self.assertTrue(himg.active)
        self.assertFalse(himg.use_button)
        self.assertEqual(himg.teaser_text, "Buy Now!")
        self.assertEqual(himg.button_text, "Gas Offers")
        self.assertEqual(himg.button_link, "#gas")

    def test_hero_image_str_value_set_correctly(self):
        himg = HeroImage.objects.get(title="Gas Offers")
        self.assertEqual(himg.__str__(), "Gas Offers")

    def tearDown(self):
        HeroImage.objects.all().delete()


class InvoiceDeliveryTests(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            name="Customer", phone_number="+353871234567", email="customer@example.com"
        )
        self.invoice = Invoice.objects.create(customer=self.customer)

    def test_generated_invoice_ids_are_unique_and_stable(self):
        other = Invoice.objects.create(customer=self.customer)
        original_id = self.invoice.invoice_id
        self.assertEqual(len(original_id), 6)
        self.assertNotEqual(original_id, other.invoice_id)
        self.invoice.save()
        self.invoice.refresh_from_db()
        self.assertEqual(self.invoice.invoice_id, original_id)

    def test_item_display_amounts(self):
        item = InvoiceItem.objects.create(
            invoice=self.invoice,
            description="Service",
            unit_price=Decimal("100"),
            quantity=Decimal("2"),
            vat_rate=Decimal("13.5"),
        )
        self.assertEqual(str(item), "Service")
        self.assertEqual(item.total_vat_amount, "€ 27.00")
        self.assertEqual(item.total_amount, "€ 227.00")

    @patch("gbs.models.sms.send_sms", return_value={"success": True})
    def test_sms_success_marks_invoice_as_sent(self, send):
        result = self.invoice.send_sms()
        self.assertEqual(result, (True, {"success": True}))
        number, message = send.call_args.args
        self.assertEqual(number, self.customer.phone_number)
        self.assertIn(self.invoice.invoice_id, message)
        self.invoice.refresh_from_db()
        self.assertTrue(self.invoice.invoiced)

    @patch("gbs.models.sms.send_sms", return_value={"success": False})
    def test_sms_failure_does_not_mark_invoice_as_sent(self, send):
        self.assertEqual(self.invoice.send_sms(), (False, {"success": False}))
        send.assert_called_once()
        self.invoice.refresh_from_db()
        self.assertFalse(self.invoice.invoiced)

    @patch("gbs.models.sms.send_sms")
    def test_missing_phone_does_not_attempt_sms(self, send):
        self.customer.phone_number = ""
        self.customer.save()
        self.assertEqual(self.invoice.send_sms(), (False, None))
        send.assert_not_called()
        self.invoice.refresh_from_db()
        self.assertFalse(self.invoice.invoiced)

    def test_email_delivery_marks_invoice_as_sent(self):
        self.invoice.send_invoice()
        self.invoice.refresh_from_db()
        self.assertTrue(self.invoice.invoiced)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(self.invoice.invoice_id, mail.outbox[0].subject)
        self.assertEqual(len(mail.outbox[0].attachments), 1)

    @patch("gbs.models.email.send_invoice", side_effect=OSError("Mail unavailable"))
    def test_email_error_does_not_mark_invoice_as_sent(self, send):
        with self.assertRaisesMessage(OSError, "Mail unavailable"):
            self.invoice.send_invoice()
        self.invoice.refresh_from_db()
        self.assertFalse(self.invoice.invoiced)
