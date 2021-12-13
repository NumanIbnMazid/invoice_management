from django import forms
from utils.mixins import CustomModelForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


class UserManageForm(CustomModelForm):
    
    email = forms.EmailField(
        label='Email', max_length=255, help_text="Enter valid email...", widget=forms.EmailInput(attrs={'placeholder': 'Enter email...'})
    )
    password = forms.CharField(
        label='Password', max_length=100, help_text="Enter strong password", widget=forms.PasswordInput(attrs={'placeholder': 'Enter password...'})
    )
    confirm_password = forms.CharField(
        label='Confirm Password', max_length=100, help_text="Enter password again", widget=forms.PasswordInput(attrs={'placeholder': 'Enter password again...'})
    )
    
    class Meta:
        model = get_user_model()
        fields = ['name', 'email', 'password', 'confirm_password']

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email

    

class UserUpdateForm(CustomModelForm):
    class Meta:
        model = get_user_model()
        fields = ['payment_permission']

    