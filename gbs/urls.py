from django.urls import path
from .admin import admin_site
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin_site.urls),
]
