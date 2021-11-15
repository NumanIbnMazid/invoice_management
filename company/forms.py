from django import forms
from utils.mixins import CustomSimpleForm, CustomModelForm
from .models import Company
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from django.db.models.fields.files import ImageFieldFile
from django.template.defaultfilters import filesizeformat
import os
from ckeditor.widgets import CKEditorWidget


class DateInput(forms.DateInput):
    input_type = 'date'


class CompanyCreateForm(CustomModelForm):
    
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
        model = Company
        fields = ['name', 'logo', 'registration_date', 'is_active', 'description']
        widgets = {
            # 'description': CKEditorWidget(),
            'description': forms.Textarea(attrs={'rows': 3, 'cols': 2}),
            'registration_date': DateInput(),
        }
        
    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email
    
    def clean_logo(self):
        logo = self.cleaned_data.get('logo')
        if logo and isinstance(logo, UploadedFile):
            file_extension = os.path.splitext(logo.name)[1]
            allowed_image_types = settings.ALLOWED_IMAGE_TYPES
            content_type = logo.content_type.split('/')[0]
            if not file_extension in allowed_image_types:
                raise forms.ValidationError("Only %s file formats are supported! Current logo format is %s" % (
                    allowed_image_types, file_extension))
            if logo.size > settings.MAX_UPLOAD_SIZE:
                raise forms.ValidationError("Please keep filesize under %s. Current filesize %s" % (
                    filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(logo.size)))
            return logo
        return None

    def clean(self):
        form_data = self.cleaned_data
        if form_data['password'] != form_data['confirm_password']:
            self._errors["password"] = ["Password do not match"]
            del form_data['password']
        return form_data
    


class CompanyManageForm(CustomModelForm):
    
    class Meta:
        model = Company
        fields = ['name', 'logo', 'registration_date', 'is_active', 'description']
        widgets = {
            # 'description': CKEditorWidget(),
            'description': forms.Textarea(attrs={'rows': 3, 'cols': 2}),
            'registration_date': DateInput(),
        }
        
    def clean_logo(self):
        logo = self.cleaned_data.get('logo')
        if logo and isinstance(logo, UploadedFile):
            file_extension = os.path.splitext(logo.name)[1]
            allowed_image_types = settings.ALLOWED_IMAGE_TYPES
            content_type = logo.content_type.split('/')[0]
            if not file_extension in allowed_image_types:
                raise forms.ValidationError("Only %s file formats are supported! Current logo format is %s" % (
                    allowed_image_types, file_extension))
            if logo.size > settings.MAX_UPLOAD_SIZE:
                raise forms.ValidationError("Please keep filesize under %s. Current filesize %s" % (
                    filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(logo.size)))
            return logo
        return None
