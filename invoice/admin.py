from django.contrib import admin
from utils.mixins import CustomModelAdminMixin
from .models import Invoice


# class InvoiceAdmin(CustomModelAdminMixin, admin.ModelAdmin):
#     pass

#     class Meta:
#         model = Invoice

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("get_company", "coupon", "vat", "additional_charge", "total_cost", "status", "created_at")

    class Meta:
        model = Invoice


admin.site.register(Invoice, InvoiceAdmin)
