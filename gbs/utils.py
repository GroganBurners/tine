from django.http import HttpResponse

def excel_response(xls_funk, file_name, *args, **kwargs):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="'+file_name+'"'
    xls_funk(response, *args, **kwargs)
    return response



def pdf_response(pdf_funk, file_name, *args, **kwargs):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="'+file_name+'"'
    pdf_funk(response, *args, **kwargs)
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
