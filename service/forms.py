from django import forms
from utils.mixins import CustomSimpleForm, CustomModelForm
from .models import Service


class DateInput(forms.DateInput):
    input_type = 'date'

class ServiceManageForm(CustomModelForm):
    class Meta:
        model = Service
        fields = ['name', 'company', 'price', 'registration_date', 'due_date', 'is_active']
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
