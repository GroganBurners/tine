import logging
import zipfile
from io import BytesIO

from django.http import HttpResponse

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


def get_season():
    from datetime import date

    doy = date.today().timetuple().tm_yday
    # "day of year" ranges for the northern hemisphere
    spring = range(80, 172)
    summer = range(172, 264)
    autumn = range(264, 355)
    # winter = everything else

    if doy in spring:
        season = "spring"
    elif doy in summer:
        season = "summer"
    elif doy in autumn:
        season = "autumn"
    else:
        season = "winter"
    return season
