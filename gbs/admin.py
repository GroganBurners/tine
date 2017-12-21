from django.contrib import admin
from .models import Carousel, Customer, Expense, ExpenseType, Service, Supplier, Price

class ServiceInline(admin.TabularInline):
        model = Service

class CustomerAdmin(admin.ModelAdmin):
    model = Customer
    inlines = [ServiceInline,]
    list_display = ['name', 'street', 'county']
    search_fields = ('name', 'street')

class ExpenseAdmin(admin.ModelAdmin):
    model = Expense
    autocomplete_fields = ['type','supplier']
    list_display = ['supplier', 'cost', 'vat']
    search_fields = ('supplier', 'cost')

class ExpenseTypeAdmin(admin.ModelAdmin):
    model = ExpenseType
    search_fields = ['type']

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}

class PriceAdmin(admin.ModelAdmin):
    model = Price
    list_display = ['type', 'cost', 'summer_offer']

class SupplierAdmin(admin.ModelAdmin):
    model = Supplier
    list_display = ['name', 'email', 'phone_number']
    search_fields = ('name', 'email')

class CarouselAdmin(admin.ModelAdmin):
    model = Carousel
    ordering = ('active','order')
    list_display = ['active', 'order', 'title', 'image', 'teaser_text']

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Carousel, CarouselAdmin)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(ExpenseType, ExpenseTypeAdmin)
admin.site.register(Price, PriceAdmin)
admin.site.register(Supplier, SupplierAdmin)
