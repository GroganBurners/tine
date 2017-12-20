from django.urls import path

from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('export/xls/', views.export_finance_xls, name='export_finance_xls'),
]
