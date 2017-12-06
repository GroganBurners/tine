from django.contrib import admin
from .models import Customer, Service, Price

class ServiceInline(admin.TabularInline):
        model = Service

class CustomerAdmin(admin.ModelAdmin):
    model = Customer
    inlines = [ServiceInline,]
    list_display = ['first_name', 'last_name']
    search_fields = ('first_name', 'last_name')

class PriceAdmin(admin.ModelAdmin):
    model = Price
    list_display = ['type', 'cost', 'summer_offer']


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Price, PriceAdmin)
