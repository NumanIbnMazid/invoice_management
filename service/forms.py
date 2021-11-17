from django import forms
from utils.mixins import CustomSimpleForm, CustomModelForm
from .models import Service
from company.models import Company
from django_select2.forms import ModelSelect2Widget


class DateInput(forms.DateInput):
    input_type = 'date'

class ServiceManageForm(CustomModelForm):
    
    company = forms.ModelChoiceField(
        queryset=Company.objects.filter(is_active=True),
        label=u"Company",
        empty_label="Select Company...",
        widget=ModelSelect2Widget(
            model=Company,
            search_fields=['name__icontains'],
            max_results=500,
            attrs={'data-minimum-input-length': '0'}
        )
    )
    class Meta:
        model = Service
        fields = ['name', 'company', 'price', 'currency', 'registration_date', 'due_date', 'is_active']
        widgets = {
            'registration_date': DateInput(),
            'due_date': DateInput(),
        }
        
    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        registration_date = self.cleaned_data.get('registration_date')
        
        if registration_date == None or registration_date == "":
            raise forms.ValidationError("Registration Date is required!")
        
        if not due_date == None:
            if not due_date > registration_date:
                raise forms.ValidationError("Due Date must be greater than Registration Date!")
            
        return due_date
