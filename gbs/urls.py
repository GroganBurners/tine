from django.urls import path

from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('admin/export/xls/', views.export_finance_xls, name='export_finance_xls'),
  path('admin/export/pdf/invoice/<int:id>/', views.print_invoice, name='print_invoice'),
]
