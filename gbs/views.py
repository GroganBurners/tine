from decimal import Decimal

from django.shortcuts import render

from gbs.models import HeroImage, Price
from gbs.utils import get_season

ADMIN_LOGIN_URL = "/admin/login/"


def index(request):
    gas_prices = Price.objects.filter(
        type__startswith="gas", summer_offer=False, cost__gt=Decimal("0.00")
    ).exclude(type__endswith="install")
    oil_prices = Price.objects.filter(
        type__startswith="oil", summer_offer=False, cost__gt=Decimal("0.00")
    )

    repair_fees = Price.objects.filter(
        type__startswith="repair", summer_offer=False, cost__gt=Decimal("0.00")
    )

    summer_repair = Price.objects.filter(
        type__startswith="repair", summer_offer=False, cost__gt=Decimal("0.00")
    )

    summer_gas = Price.objects.filter(
        type__startswith="gas", summer_offer=True, cost__gt=Decimal("0.00")
    )
    summer_oil = Price.objects.filter(
        type__startswith="oil", summer_offer=True, cost__gt=Decimal("0.00")
    )

    active_heroes = HeroImage.objects.filter(active=True).order_by("pk")
    hero = active_heroes.filter(season=get_season()).first()
    if hero is None:
        hero = active_heroes.filter(season="").first()
    context = {
        "hero": hero,
        "gas_prices": gas_prices,
        "oil_prices": oil_prices,
        "summer_gas": summer_gas,
        "summer_oil": summer_oil,
        "repair_fees": repair_fees,
        "summer_repair": summer_repair,
    }
    return render(request, "index.html", context)
