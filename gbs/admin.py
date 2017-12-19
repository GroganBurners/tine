from django.contrib import admin
from .models import Carousel, Customer, Service, Price

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

class CarouselAdmin(admin.ModelAdmin):
    model = Carousel
    ordering = ('-active','-order')
    list_display = ['active', 'order', 'title', 'image', 'teaser_text']

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Carousel, CarouselAdmin)
admin.site.register(Price, PriceAdmin)
