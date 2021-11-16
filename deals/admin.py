from django.contrib import admin
from utils.mixins import CustomModelAdminMixin
from .models import Coupon, Vat


class CouponAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

    class Meta:
        model = Coupon


admin.site.register(Coupon, CouponAdmin)


class VatAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

    class Meta:
        model = Vat


admin.site.register(Vat, VatAdmin)
