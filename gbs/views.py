from django.shortcuts import get_object_or_404, render
from gbs.models import Carousel, Price, Invoice
from decimal import Decimal
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from gbs.utils import excel_response, pdf_response
from gbs.excel import export_finances
from gbs.pdf import export_invoice
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
    repair_fee = Price.objects.filter(type__startswith="repair",
                                      cost__gt=Decimal('0.00'))[0]
    # season = get_season()
    carousels = Carousel.objects.filter(active=True).order_by('order')
    context = { 'carousels': carousels, 'gas_prices': gas_prices, 
                'oil_prices': oil_prices, 'summer_gas': summer_gas, 
                'summer_oil': summer_oil, 'repair_fee': repair_fee }
    return render(request, 'index.html', context)

@login_required(login_url=ADMIN_LOGIN_URL)
def export_finance_xls(request):
    return excel_response(export_finances, "FinanceSheet.xlsx")

@login_required(login_url=ADMIN_LOGIN_URL)
def print_invoice(request, id):
    invoice = get_object_or_404(Invoice, id=id)
    return pdf_response(export_invoice, "Invoice.pdf", invoice)

