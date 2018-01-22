from django.shortcuts import render
from gbs.models import Carousel, Price
from decimal import Decimal
ADMIN_LOGIN_URL = '/admin/login/'


# Create your views here.
def index(request):
    gas_prices = Price.objects.filter(type__startswith="gas",
                                      summer_offer=False,
                                      cost__gt=Decimal('0.00')
                                      ).exclude(type__endswith="install")
    oil_prices = Price.objects.filter(type__startswith="oil",
                                      summer_offer=False,
                                      cost__gt=Decimal('0.00'))
    summer_gas = Price.objects.filter(type__startswith="gas",
                                      summer_offer=True,
                                      cost__gt=Decimal('0.00'))
    summer_oil = Price.objects.filter(type__startswith="oil",
                                      summer_offer=True,
                                      cost__gt=Decimal('0.00'))
    repair_fees = Price.objects.filter(type__startswith="repair",
                                      cost__gt=Decimal('0.00'))
    # season = get_season()
    carousels = Carousel.objects.filter(active=True).order_by('order')
    context = {'carousels': carousels, 'gas_prices': gas_prices,
               'oil_prices': oil_prices, 'summer_gas': summer_gas,
               'summer_oil': summer_oil, 'repair_fees': repair_fees}
    return render(request, 'index.html', context)

def newindex(request):
    gas_prices = Price.objects.filter(type__startswith="gas",
                                      summer_offer=False,
                                      cost__gt=Decimal('0.00')
                                      ).exclude(type__endswith="install")
    oil_prices = Price.objects.filter(type__startswith="oil",
                                      summer_offer=False,
                                      cost__gt=Decimal('0.00'))
    summer_gas = Price.objects.filter(type__startswith="gas",
                                      summer_offer=True,
                                      cost__gt=Decimal('0.00'))
    summer_oil = Price.objects.filter(type__startswith="oil",
                                      summer_offer=True,
                                      cost__gt=Decimal('0.00'))
    repair_fees = Price.objects.filter(type__startswith="repair",
                                      cost__gt=Decimal('0.00'))
    # season = get_season()
    carousels = Carousel.objects.filter(active=True).order_by('order')
    context = {'carousels': carousels, 'gas_prices': gas_prices,
               'oil_prices': oil_prices, 'summer_gas': summer_gas,
               'summer_oil': summer_oil, 'repair_fees': repair_fees}
    return render(request, 'new/index.html', context)
