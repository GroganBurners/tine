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
