from django.contrib import admin, messages
from django.contrib.admin import AdminSite
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.utils.html import format_html

from .export.excel_export import export_finances
from .export.pdf import export_invoice
from .models import (
    Customer,
    Expense,
    ExpenseItem,
    ExpenseType,
    HeroImage,
    Invoice,
    InvoiceItem,
    Price,
    Supplier,
)
from .utils import excel_response, pdf_response, zip_response
from django_celery_beat.models import PeriodicTask, IntervalSchedule


class GBSAdminSite(AdminSite):
    site_header = "Grogan Burner Services Admin Site"

    def export_finances_xls(self, request):
        return excel_response(export_finances, "FinanceSheetExport.xlsx")

    def get_urls(self):
        return [
            path(
                "export/xls/",
                self.admin_view(self.export_finances_xls),
                name="export-finances",
            ),
        ] + super().get_urls()


admin_site = GBSAdminSite(name="gbsadmin")


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1


class InvoiceAdmin(admin.ModelAdmin):
    autocomplete_fields = ["customer"]
    readonly_fields = ("invoice_id",)
    inlines = [InvoiceItemInline]
    list_display = [
        "invoice_id",
        "customer",
        "date",
        "draft",
        "invoiced",
        "paid_date",
        "total",
        "invoice_actions",
    ]
    search_fields = ("invoice_id", "customer__name")
    actions = ["email_invoices", "print_invoices"]
    model = Invoice

    def print_invoice(self, request, invoice_id):
        invoice = self.get_object(request, invoice_id)
        return pdf_response(export_invoice, invoice.file_name(), invoice)

    def print_invoices(self, request, queryset):
        files = []
        for invoice in queryset.all():
            pdf = export_invoice(invoice)
            files.append((invoice.file_name(), pdf))

        return zip_response(files, "invoice.zip")

    print_invoices.short_description = "Generate a Zip of PDF invoice(s)"

    def sms_invoice(self, request, invoice_id):
        invoice = self.get_object(request, invoice_id)
        if invoice.customer.phone_number:
            if invoice.send_sms():
                messages.add_message(request, messages.INFO, "Invoice SMS Sent.")
            else:
                messages.add_message(
                    request,
                    messages.ERROR,
                    "SMS sending failed. Please check the logs and try later.",
                )
        else:
            messages.add_message(
                request, messages.ERROR, "No phone number present for customer."
            )
        return HttpResponseRedirect("../")

    def email_invoice(self, request, invoice_id):
        invoice = self.get_object(request, invoice_id)
        invoice.send_invoice()
        messages.add_message(request, messages.INFO, "Invoice Email Sent.")
        return HttpResponseRedirect("../")

    def email_invoices(self, request, queryset):
        for invoice in queryset.all():
            invoice.send_invoice()

    email_invoice.short_description = "Send invoice to client"

    def get_urls(self):
        return [
            path(
                "<int:invoice_id>/pdf/",
                self.admin_site.admin_view(self.print_invoice),
                name="invoice-pdf",
            ),
            path(
                "<int:invoice_id>/email/",
                self.admin_site.admin_view(self.email_invoice),
                name="invoice-email",
            ),
            path(
                "<int:invoice_id>/sms/",
                self.admin_site.admin_view(self.sms_invoice),
                name="invoice-sms",
            ),
        ] + super().get_urls()

    def invoice_actions(self, obj):
        return format_html(
            '<a class="button" href="{}">PDF</a> \
             <a class="button" href="{}">Email</a> \
             <a class="button" href="{}">SMS</a>',
            reverse("gbsadmin:invoice-pdf", args=[obj.pk]),
            reverse("gbsadmin:invoice-email", args=[obj.pk]),
            reverse("gbsadmin:invoice-sms", args=[obj.pk]),
        )

    invoice_actions.short_description = "Invoice Actions"
    invoice_actions.allow_tags = True


class CustomerAdmin(admin.ModelAdmin):
    model = Customer
    list_display = ["name", "street", "county"]
    search_fields = ("name", "street")


class ExpenseItemInline(admin.TabularInline):
    model = ExpenseItem
    extra = 1


class ExpenseAdmin(admin.ModelAdmin):
    model = Expense
    inlines = [ExpenseItemInline]
    autocomplete_fields = ["type", "supplier"]
    list_display = ["date", "supplier", "total"]
    search_fields = ("supplier", "total")


class ExpenseTypeAdmin(admin.ModelAdmin):
    model = ExpenseType
    search_fields = ["type"]

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


class PriceAdmin(admin.ModelAdmin):
    model = Price
    list_display = ["type", "cost", "summer_offer"]


class SupplierAdmin(admin.ModelAdmin):
    model = Supplier
    list_display = ["name", "email", "phone_number"]
    search_fields = ("name", "email")


class HeroImageAdmin(admin.ModelAdmin):
    model = HeroImage
    ordering = ("title", "active")
    list_display = ["title", "active", "image", "teaser_text"]


admin_site.register(Customer, CustomerAdmin)
admin_site.register(Expense, ExpenseAdmin)
admin_site.register(ExpenseType, ExpenseTypeAdmin)
admin_site.register(HeroImage, HeroImageAdmin)
admin_site.register(Invoice, InvoiceAdmin)
admin_site.register(Price, PriceAdmin)
admin_site.register(Supplier, SupplierAdmin)
admin_site.register(PeriodicTask)
admin_site.register(IntervalSchedule)
