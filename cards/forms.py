from utils.mixins import CustomModelForm
from .models import Card
from utils.models import Configuration
from django import forms
from utils.custom_form_widgets import MonthYearWidget


class CardManageForm(CustomModelForm):
    
    expire_date = forms.DateTimeField(required=True, label='Expire Date', widget=MonthYearWidget())
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CardManageForm, self).__init__(*args, **kwargs)

        if len(Configuration.objects.all()) > 0:
            self.initial['payment_amount'] = Configuration.objects.last().payment_amount
            
    class Meta:
        model = Card
        fields = ['card_type', 'company_name', 'name_on_card', 'card_number', 'cvc', 'expire_date', 'payment_amount', 'save_card']