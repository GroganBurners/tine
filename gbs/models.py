from django.db import models
from django.core.validators import RegexValidator


class Supplier(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone" +
                                 " number must be entered in the format:" +
                                 " '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=16,
                                    blank=True)
    COUNTIES = (
        ('C', 'Cork'),
        ('CE', 'Clare'),
        ('CN', 'Cavan'),
        ('CW', 'Carlow'),
        ('D', 'Dublin'),
        ('DL', 'Donegal'),
        ('G', 'Galway'),
        ('KE', 'Kildare'),
        ('KK', 'Kilkenny'),
        ('KY', 'Kerry'),
        ('L', 'Limerick'),
        ('LD', 'Longford'),
        ('LH', 'Louth'),
        ('LM', 'Leitrim'),
        ('LS', 'Loais'),
        ('MH', 'Meath'),
        ('MM', 'Monaghan'),
        ('MO', 'Mayo'),
        ('OY', 'Offaly'),
        ('RN', 'Roscommon'),
        ('SO', 'Sligo'),
        ('T', 'Tipperary'),
        ('W', 'Waterford'),
        ('WH', 'Westmeath'),
        ('WX', 'Wexford'),
        ('WW', 'Wicklow'),
    )
    street = models.CharField(max_length=200, blank=True)
    county = models.CharField(choices=COUNTIES, max_length=30, blank=True, default='KK')
    eircode = models.CharField(max_length=12, blank=True, default='R95 XXXX')
    country = models.CharField(max_length=200, blank=True, default='Ireland')
    date_added = models.DateField(auto_now=True)
    date_updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

class ExpenseType(models.Model):
    type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.type

class Expense(models.Model):
    type = models.ForeignKey(ExpenseType, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=6, decimal_places=2)
    vat = models.DecimalField(max_digits=6, decimal_places=2)
    notes = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone" +
                                 " number must be entered in the format:" +
                                 " '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=16,
                                    blank=True)
    COUNTIES = (
        ('C', 'Cork'),
        ('CE', 'Clare'),
        ('CN', 'Cavan'),
        ('CW', 'Carlow'),
        ('D', 'Dublin'),
        ('DL', 'Donegal'),
        ('G', 'Galway'),
        ('KE', 'Kildare'),
        ('KK', 'Kilkenny'),
        ('KY', 'Kerry'),
        ('L', 'Limerick'),
        ('LD', 'Longford'),
        ('LH', 'Louth'),
        ('LM', 'Leitrim'),
        ('LS', 'Loais'),
        ('MH', 'Meath'),
        ('MM', 'Monaghan'),
        ('MO', 'Mayo'),
        ('OY', 'Offaly'),
        ('RN', 'Roscommon'),
        ('SO', 'Sligo'),
        ('T', 'Tipperary'),
        ('W', 'Waterford'),
        ('WH', 'Westmeath'),
        ('WX', 'Wexford'),
        ('WW', 'Wicklow'),
    )
    street = models.CharField(max_length=200, blank=True)
    county = models.CharField(choices=COUNTIES, max_length=30, blank=True)
    eircode = models.CharField(max_length=12, blank=True)
    date_added = models.DateField(auto_now=True)
    date_updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.first_name + " " + self.last_name + "(" + street + ")"


class Service(models.Model):
    TYPES = (
        # Start of GAS Categories
        ('gas_service', 'Gas Service'),
        ('gas_combi_service', 'Gas Combi/Condensing Boiler Service'),
        ('gas_fire', 'Gas Fire Service'),
        ('gas_service_fire', 'Gas Boiler and Fire service together'),
        ('gas_install', 'Gas Install'),
        # Start of OIL Categories
        ('oil_service', 'Oil Service'),
        ('oil_combi_service', 'Oil Combi/Condensing Service'),
        ('oil_install', 'Oil Install'),
        # Start of Repair Categories
        ('repair_call_out', 'Repair Call Out Fee (First Hour)'),
        # Start of BER Categories
        ('ber', 'Building Energy Rating'),
    )
    type = models.CharField(choices=TYPES, max_length=30)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total = models.DecimalField(max_digits=6, decimal_places=2)
    vat = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        desc = "Service No: " + str(self.id) + " (" + str(self.customer) + ")"
        return desc


class Price(models.Model):
    type = models.CharField(choices=Service.TYPES, max_length=30)
    cost = models.DecimalField(max_digits=6, decimal_places=2)
    summer_offer = models.BooleanField()

    def __str__(self):
        d = dict(Service.TYPES)
        ser_name = d[self.type]
        return ser_name + " " + "€" + ('%f' % self.cost).rstrip('0').rstrip('.')

class Carousel(models.Model):
    title = models.CharField(max_length=50, blank=False, null=False)
    image = models.ImageField(upload_to='%Y/%m', blank=False, null=False)
    teaser_text = models.CharField(max_length=200, blank=False, null=False)
    active = models.BooleanField(blank=False, null=False, default=False)
    order = models.PositiveSmallIntegerField(blank=False, null=False)
    use_button = models.BooleanField()
    button_text = models.CharField(max_length=50)
    button_link = models.CharField(max_length=20)

    def __str__(self):
        return self.title
