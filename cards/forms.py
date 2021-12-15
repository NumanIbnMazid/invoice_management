from utils.mixins import CustomModelForm
from .models import Card
from utils.models import Configuration
from django import forms
from utils.custom_form_widgets import MonthYearWidget


class CardManageForm(CustomModelForm):
    
    expire_date = forms.DateTimeField(required=True, label='Expire Date', widget=MonthYearWidget())
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.object = kwargs.pop('object', None)
        super(CardManageForm, self).__init__(*args, **kwargs)

        if len(Configuration.objects.all()) > 0 and not self.object:
            self.initial['payment_amount'] = Configuration.objects.last().payment_amount if Configuration.objects.last().is_active else None
            
        # card fields
        # self.fields["name_on_card"].widget.attrs.update({'class': 'payment-cardname form-control', 'data-id': 'payment-cardname'})
        # self.fields["card_number"].widget.attrs.update({'class': 'payment-cardnumber form-control', 'data-id': 'payment-cardnumber'})
        # self.fields["expire_date"].widget.attrs.update({'class': 'expirydate form-control', 'data-id': 'expirydate'})
        # self.fields["cvc"].widget.attrs.update({'class': 'cvvnumber form-control', 'data-id': 'cvvnumber'})
            
    class Meta:
        model = Card
        fields = ['card_type', 'company_name', 'name_on_card', 'card_number', 'cvc', 'expire_date', 'payment_amount', 'save_card']