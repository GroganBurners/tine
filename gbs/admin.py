from django.contrib import admin
from .models import Carousel, Customer, Expense, ExpenseType, Invoice, InvoiceItem, Supplier, Price

class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem

class InvoiceAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    readonly_fields=('invoice_id',)
    inlines = [ InvoiceItemInline ]
    list_display = [
        'invoice_id', 
        'customer', 
        'invoice_date', 
        'draft', 
        'invoiced',
        'paid_date',
        'total'
    ]
    search_fields = ('invoice_id', 'customer__name')
    model = Invoice

class CustomerAdmin(admin.ModelAdmin):
    model = Customer
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
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Price, PriceAdmin)
admin.site.register(Supplier, SupplierAdmin)
