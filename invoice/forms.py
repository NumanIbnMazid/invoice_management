from django import forms
from utils.mixins import CustomModelForm
from .models import Invoice
from deals.models import Coupon, Vat


class InvoiceManageForm(CustomModelForm):
    class Meta:
        model = Invoice
        fields = "__all__"
        exclude = ('slug', 'total_cost', 'created_at', 'created_at')

    def clean_coupon(self):
        coupon = self.cleaned_data.get('coupon')

        if not coupon == None:
            qs = Coupon.objects.filter(code__iexact=coupon.code)
            if not qs:
                raise forms.ValidationError("Invalid Coupon!")
            if qs and not qs.last().is_active:
                raise forms.ValidationError("Coupon Expired!")

        return coupon

    def clean_vat(self):
        vat = self.cleaned_data.get('vat')

        if not vat == None:
            qs = Vat.objects.filter(slug__iexact=vat.slug)
            if not qs:
                raise forms.ValidationError("Vat not exists!")
            if qs and not qs.last().is_active:
                raise forms.ValidationError("Vat is not active!")

        return vat
