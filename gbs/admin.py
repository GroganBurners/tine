from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.html import format_html
from django.urls import reverse, path
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from .models import Carousel, Customer, Expense, ExpenseType, Invoice, InvoiceItem, Supplier, Price
from gbs.utils import excel_response, pdf_response
from gbs.pdf import export_invoice

class GBSAdminSite(AdminSite):
    site_header = "Grogan Burner Services Admin Site"

admin_site = GBSAdminSite(name="gbsadmin")

class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem

class InvoiceAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    readonly_fields=('invoice_id',)
    inlines = [ InvoiceItemInline ]
    list_display = [
        'invoice_id', 'customer', 'invoice_date', 
        'draft', 'invoiced', 'paid_date', 'total',
        'invoice_actions'
    ]
    search_fields = ('invoice_id', 'customer__name')
    actions = ['send_invoice', 'print_invoice']
    model = Invoice

    def print_invoice(self, request, invoice_id):
        invoice = self.get_object(request, invoice_id)
        return pdf_response(export_invoice, invoice.file_name(), invoice)

    print_invoice.short_description = "Generate PDF of invoice"

    def email_invoice(self, request, invoice_id):
        invoice = self.get_object(request, invoice_id)
        invoice.send_invoice()
        messages.add_message(request, messages.INFO, 'Invoice Email Sent.')
        return HttpResponseRedirect("../")

    def email_invoices(self, request, queryset):
        for invoice in queryset.all():
            invoice.send_invoice()

    email_invoice.short_description = "Send invoice to client"

    def get_urls(self):
        return [
                path('<int:invoice_id>/pdf/',
                    self.admin_site.admin_view(self.print_invoice),
                    name='invoice-pdf'
                    ),
                path('<int:invoice_id>/email/',
                    self.admin_site.admin_view(self.email_invoice),
                    name='invoice-email'
                    ),
                path('email/',
                    self.admin_site.admin_view(self.email_invoices),
                    name='invoice-emails'
                    )
        ] + super().get_urls()

    def invoice_actions(self, obj):
        return format_html(
            '<a class="button" href="{}">PDF</a>',
            reverse('gbsadmin:invoice-pdf', args=[obj.pk]),
            '<a class="button" href="{}">Email</a>',
            reverse('gbsadmin:invoice-email', args=[obj.pk]),
        )
    invoice_actions.short_description = 'Invoice Actions'
    invoice_actions.allow_tags = True

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
    list_display = ['title', 'active', 'order', 'image', 'teaser_text']

admin_site.register(Customer, CustomerAdmin)
admin_site.register(Carousel, CarouselAdmin)
admin_site.register(Expense, ExpenseAdmin)
admin_site.register(ExpenseType, ExpenseTypeAdmin)
admin_site.register(Invoice, InvoiceAdmin)
admin_site.register(Price, PriceAdmin)
admin_site.register(Supplier, SupplierAdmin)
