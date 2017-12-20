from django.shortcuts import render
from gbs.models import Carousel, Price
from decimal import Decimal
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Working with Excel
from openpyxl import Workbook
from openpyxl.compat import range
from openpyxl.utils import get_column_letter


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
    repair_fee = Price.objects.filter(type__startswith="repair",
                                      cost__gt=Decimal('0.00'))[0]
    # season = get_season()
    carousels = Carousel.objects.filter(active=True).order_by('order')
    context = { 'carousels': carousels, 'gas_prices': gas_prices, 
                'oil_prices': oil_prices, 'summer_gas': summer_gas, 
                'summer_oil': summer_oil, 'repair_fee': repair_fee }
    return render(request, 'index.html', context)

@login_required
def export_finance_xls(request):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="FinanceSheet.xlsx"'

    wb = Workbook()
    ws = wb.active
    ws.title = "FinanceSheet2017"

    # Sheet header, first row
    row_num = 0

    ws.append(['Date', 'Details', 'Company', 'Money Out', 'Money In', 'VAT Due In', 'VAT Due Out', 'VAT Total', 'Total' ])


    rows = User.objects.all().values_list('username', 'first_name', 'last_name', 'email')
    for row in rows:
        ws.append(row)

    wb.save(response)
    return response


def get_season():
    from datetime import date
    doy = date.today().timetuple().tm_yday
    # "day of year" ranges for the northern hemisphere
    spring = range(80, 172)
    summer = range(172, 264)
    autumn = range(264, 355)
    # winter = everything else

    if doy in spring:
        season = 'spring'
    elif doy in summer:
        season = 'summer'
    elif doy in autumn:
        season = 'autumn'
    else:
        season = 'winter'
    return season
