from django import forms
from utils.mixins import CustomModelForm
from .models import Invoice
from deals.models import Coupon, Vat
from company.models import Company
from service.models import Service
from django_select2.forms import ModelSelect2MultipleWidget, ModelSelect2Widget



class InvoiceManageForm(CustomModelForm):
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.object = kwargs.pop('object', None)
        super(InvoiceManageForm, self).__init__(*args, **kwargs)
        
        if self.object:
            self.initial['company'] = self.object.service.first().company
            
    try:
    
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

        service = forms.ModelMultipleChoiceField(
            queryset=Service.objects.all(),
            label=u"Service",
            widget=ModelSelect2MultipleWidget(
                model=Service,
                search_fields=['name__icontains', 'company__name__icontains'],
                dependent_fields={'company': 'company'},
                max_results=500,
                attrs={'data-minimum-input-length': '0'}
            )
        )
        
        coupon = forms.ModelChoiceField(
            queryset=Coupon.objects.filter(is_active=True),
            required=False,
            label=u"Coupon",
            empty_label="Select Coupon...",
            widget=ModelSelect2Widget(
                model=Coupon,
                search_fields=['code__icontains', 'discount_amount__icontains'],
                max_results=500,
                attrs={'data-minimum-input-length': '0'}
            )
        )
        
        vat = forms.ModelChoiceField(
            queryset=Vat.objects.filter(is_active=True),
            required=False,
            initial=Vat.objects.filter(is_active=True).last(),
            label=u"Vat",
            empty_label="Select Vat..."
        )
    except Exception as e:
        
        print("*********** Exception: Invoice->forms.py: ", e, "***********")
    
    class Meta:
        model = Invoice
        fields = ("company", "service", "coupon", "vat", "additional_charge", "status")
        exclude = ('slug', 'total_cost', 'created_at', 'created_at')
        

    def clean_company(self):
        company = self.cleaned_data.get('company')

        if not company:
            raise forms.ValidationError("Company is required!!")

        return company

    def clean_service(self):
        service = self.cleaned_data.get('service')

        if not service == None:
            company_ids = service.all().values_list('company', flat=True)
            if len(set(company_ids)) > 1:
                raise forms.ValidationError("Services should belong to same company!")

        return service

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
