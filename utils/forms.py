from django import forms
from utils.mixins import CustomSimpleForm, CustomModelForm
from .models import Configuration
from django_select2.forms import ModelSelect2Widget


class DateInput(forms.DateInput):
    input_type = 'date'


class ConfigurationManageForm(CustomModelForm):

    class Meta:
        model = Configuration
        fields = ['payment_amount', 'currency', 'card_page_title', 'is_active']