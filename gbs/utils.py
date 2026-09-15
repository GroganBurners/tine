import logging
import zipfile
from io import BytesIO
from zoneinfo import ZoneInfo

from django.http import HttpResponse
from django.utils import timezone

from .conf import settings

logger = logging.getLogger(__name__)


def generate_zip(files):
    mf = BytesIO()

    with zipfile.ZipFile(mf, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            zf.writestr(f[0], f[1])

    return mf.getvalue()


def excel_response(xls_funk, file_name, *args, **kwargs):
    xls = xls_funk(*args, **kwargs)
    response = HttpResponse(
        xls,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = 'attachment; filename="' + file_name + '"'
    logger.info("Generating Excel Export File: " + file_name)
    return response


def pdf_response(pdf_funk, file_name, *args, **kwargs):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="' + file_name + '"'
    logger.info("Generating PDF Export File: " + file_name)
    pdf = pdf_funk(*args, **kwargs)
    response.write(pdf)
    return response


def zip_response(files, file_name, *args, **kwargs):
    zip_file = generate_zip(files, *args, **kwargs)
    response = HttpResponse(zip_file, content_type="application/zip")
    response["Content-Disposition"] = 'attachment; filename="' + file_name + '"'
    return response


def format_currency(amount):
    sym = settings.CURRENCY_SYMBOL
    return f"{sym} {amount:.2f}"


def get_season(on_date=None):
    """Return the meteorological season for today's date in Ireland."""
    if on_date is None:
        on_date = timezone.localdate(timezone=ZoneInfo("Europe/Dublin"))
    if 3 <= on_date.month <= 5:
        return "spring"
    if 6 <= on_date.month <= 8:
        return "summer"
    if 9 <= on_date.month <= 11:
        return "autumn"
    return "winter"
