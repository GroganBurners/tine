from django.db import models
from django.core.validators import RegexValidator
from django.template.loader import render_to_string, get_template
from django.template import TemplateDoesNotExist, Context
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from .constants import COUNTIES, SERVICES
from hashids import Hashids
from datetime import date
from io import BytesIO
from email.mime.application import MIMEApplication
from decimal import Decimal, ROUND_HALF_UP
from django.conf import settings
from django.core.mail import send_mail
from .conf import settings as app_settings
from gbs.pdf import export_invoice

class ContactInfo(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone" +
                                 " number must be entered in the format:" +
                                 " '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=16,
                                    blank=True)
    street = models.CharField(max_length=200, blank=True)
    county = models.CharField(choices=COUNTIES, max_length=30, blank=True, default='KK')
    eircode = models.CharField(max_length=12, blank=True, default='R95 XXXX')
    country = models.CharField(max_length=200, blank=True, default='Ireland')

    class Meta:
        abstract = True

class Customer(ContactInfo):
    def __str__(self):
        return self.name + " (" + self.street + ")"

class Supplier(ContactInfo):
    def __str__(self):
        return self.name

class ExpenseType(models.Model):
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.type

class Expense(models.Model):
    type = models.ForeignKey(ExpenseType, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=6, decimal_places=2)
    vat = models.DecimalField(max_digits=6, decimal_places=2)
    notes = models.CharField(max_length=300)


class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    invoice_id = models.CharField(unique=True, max_length=6, null=True,
                                              blank=True, editable=False)
    invoice_date = models.DateField(default=date.today)
    invoiced = models.BooleanField(default=False)
    draft = models.BooleanField(default=False)
    paid_date = models.DateField(blank=True, null=True)

    def save(self, *args, **kwargs):
        super(Invoice, self).save(*args, **kwargs)

        if not self.invoice_id:
            hashids = Hashids(alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=6, salt='this is my salt 2')
            self.invoice_id = hashids.encode(self.id)
            super(Invoice, self).save(*args, **kwargs)

    def total_ex_vat(self):
        total = Decimal('0.00')
        for item in self.items.all():
            total = total + item.total_ex_vat()
        return total.quantize(Decimal('0.01'))

    def total_vat(self):
        total = self.total()-self.total_ex_vat()
        return total.quantize(Decimal('0.01'))

    def total(self):
        total = Decimal('0.00')
        for item in self.items.all():
            total = total + item.total()
        return total.quantize(0, ROUND_HALF_UP)

    def file_name(self):
        return f'Invoice {self.invoice_id}.pdf'

    def send_invoice(self):
        pdf = BytesIO()
        export_invoice(pdf, self)
        pdf.seek(0)
        attachment = MIMEApplication(pdf.read())
        attachment.add_header("Content-Disposition", "attachment",
                                              filename=self.file_name())
        pdf.close()

        subject = f'Your Grogan Burner Services Invoice {self.invoice_id} is ready'
        email_kwargs = {
            "invoice": self,
            "SITE_NAME": "Grogan Burner Services",
            "SUPPORT_EMAIL": app_settings.EMAIL,
        }

        # try:
        #     template = get_template("email/invoice.html")
        #     body = template.render(Context(email_kwargs))
        # except TemplateDoesNotExist:
        body = render_to_string("email/invoice.txt", email_kwargs)

        email = EmailMultiAlternatives(subject=subject, body=strip_tags(body), from_email='mick@grogan.ie', to=['neil@grogan.ie'])
        # email.attach_alternative(body, "text/html")
        email.attach(attachment)
        email.send(fail_silently=False)

        self.invoiced = True
        self.save()

    def __str__(self):
        desc = "Invoice: " + str(self.invoice_id) + " (" + str(self.customer) + ")"
        return desc

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='items', unique=False, on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    vat_rate = models.DecimalField(max_digits=5, decimal_places=2, default=13.5)
    quantity = models.DecimalField(max_digits=8, decimal_places=2, default=1)

    def total_ex_vat(self):
        total = Decimal(str(self.unit_price * self.quantity))
        return total.quantize(Decimal('0.01'))

    def total_vat(self):
        percentage = self.vat_rate/Decimal(100)
        total_ex_vat = self.total_ex_vat()
        total = Decimal(str(total_ex_vat*percentage))
        return total.quantize(Decimal('0.01'))

    def total(self):
        total = Decimal(str(self.total_ex_vat()+self.total_vat()))
        return total.quantize(Decimal('0.01'))

    def __str__(self):
        return self.description



class Price(models.Model):
    type = models.CharField(choices=SERVICES, max_length=30)
    cost = models.DecimalField(max_digits=6, decimal_places=2)
    summer_offer = models.BooleanField()

    def __str__(self):
        d = dict(SERVICES)
        ser_name = d[self.type]
        return ser_name + " " + "€" + ('%f' % self.cost).rstrip('0').rstrip('.')

class Carousel(models.Model):
    title = models.CharField(max_length=50, blank=False, null=False)
    image = models.ImageField(upload_to='images/carousel', blank=False, null=False)
    img_alt = models.CharField("Image alternative text (for screen readers)", max_length=50, blank=True, null=True)
    teaser_text = models.CharField(max_length=200, blank=False, null=False)
    active = models.BooleanField(blank=False, null=False, default=False)
    order = models.PositiveSmallIntegerField(blank=False, null=False)
    use_button = models.BooleanField()
    button_text = models.CharField(max_length=50)
    button_link = models.CharField(max_length=20)

    def __str__(self):
        return self.title
