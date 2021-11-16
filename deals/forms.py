from django import forms
from utils.mixins import CustomSimpleForm, CustomModelForm
from .models import Coupon, Vat


class DateInput(forms.DateInput):
    input_type = 'date'


class CouponManageForm(CustomModelForm):
    class Meta:
        model = Coupon
        fields = '__all__'
        exclude = ('slug', 'created_at', 'created_at')
        
    def clean_end_date(self):
        end_date = self.cleaned_data.get('end_date')
        start_date = self.cleaned_data.get('start_date')

        if start_date == None or start_date == "":
            raise forms.ValidationError("Start Date is required!")

        if not end_date == None:
            if not end_date > start_date:
                raise forms.ValidationError("End Date must be greater than Start Date!")

        return end_date
        
        
class VatManageForm(CustomModelForm):
    class Meta:
        model = Vat
        fields = '__all__'
        exclude = ('slug', 'created_at', 'created_at')
