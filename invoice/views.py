from django.views.generic import CreateView, UpdateView, DetailView, ListView
from company.models import Company
from utils.decorators import has_dashboard_permission_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.contrib import messages
from utils.helpers import (
    get_simple_context_data, get_simple_object, delete_simple_object
)
from django.conf import settings
import json
import os
from django.http import HttpResponseRedirect
# PDF imports
from django.views.generic import View
from utils.snippets import generate_pdf_with_pdfkit
from django.utils import timezone
# App Imports
from .forms import InvoiceManageForm
from .models import Invoice
from service.models import Service



dashboard_decorators = [login_required, has_dashboard_permission_required]



""" 
-------------------------------------------------------------------
                        *** Invoice ***
-------------------------------------------------------------------
"""


def get_invoice_common_contexts(request):
    extra_kwargs = {}
    STATIC_DATA_FILE = os.path.join(settings.BASE_DIR, 'utils/staticData.json')
    # Opening JSON file
    data_file = open(STATIC_DATA_FILE,)
    data = json.load(data_file)
    comapny_information = data.get("CompanyInformation", {})
    extra_kwargs.update({"company_information": comapny_information})
    # service lists
    services = Service.objects.all()
    extra_kwargs.update({"services": services})
    
    common_contexts = get_simple_context_data(
        request=request, app_namespace='invoice', model_namespace="invoice", model=Invoice, list_template="invoice/invoice-list.html", fields_to_hide_in_table=["id", "slug", "updated_at", "card_number"], **extra_kwargs
    )
    # update fields count in context
    common_contexts.update({"fields_count": common_contexts["fields_count"] + 2})
    return common_contexts


@method_decorator(dashboard_decorators, name='dispatch')
class InvoiceCreateView(CreateView):
    template_name = "admin_panel/snippets/manage.html"
    form_class = InvoiceManageForm

    def form_valid(self, form, **kwargs):
        messages.success(
            self.request, 'Invoice created successfully!'
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("invoice:create_invoice")

    def get_context_data(self, **kwargs):
        context = super(
            InvoiceCreateView, self
        ).get_context_data(**kwargs)
        context['page_title'] = 'Create Invoice'
        context['page_short_title'] = 'Create Invoice'
        for key, value in get_invoice_common_contexts(request=self.request).items():
            context[key] = value
        return context


@method_decorator(login_required, name='dispatch')
class InvoiceDetailView(DetailView):
    template_name = "invoice/invoice-detail.html"

    def get_object(self):
        return get_simple_object(key='slug', model=Invoice, self=self)
    
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        is_superuser = request.user.is_superuser
        is_company = True if self.object.service.filter(company__user=request.user).exists() else False
        if not is_superuser and not is_company:
            messages.error(
                self.request, 'Access Denied!'
            )
            return HttpResponseRedirect(reverse('home'))
        return super(InvoiceDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(
            InvoiceDetailView, self
        ).get_context_data(**kwargs)
        context['page_title'] = f'Invoice - {self.get_object().__str__()} Detail'
        context['page_short_title'] = f'Invoice - {self.get_object().__str__()} Detail'
        for key, value in get_invoice_common_contexts(request=self.request).items():
            context[key] = value
        return context


@method_decorator(dashboard_decorators, name='dispatch')
class InvoiceUpdateView(UpdateView):
    template_name = 'admin_panel/snippets/manage.html'
    form_class = InvoiceManageForm

    def get_object(self):
        return get_simple_object(key="slug", model=Invoice, self=self)
    
    def get_form_kwargs(self):
        kwargs = super(InvoiceUpdateView, self).get_form_kwargs()
        if self.form_class:
            kwargs.update({'request': self.request})
            kwargs.update({'object': self.get_object()})
        return kwargs

    def get_success_url(self):
        return reverse("invoice:create_invoice")

    def form_valid(self, form):
        messages.success(
            self.request, 'Invoice updated successfully!'
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(
            InvoiceUpdateView, self
        ).get_context_data(**kwargs)
        context['page_title'] = f'Update Invoice "{self.get_object().__str__()}"'
        context['page_short_title'] = f'Update Invoice "{self.get_object().__str__()}"'
        for key, value in get_invoice_common_contexts(request=self.request).items():
            context[key] = value
        return context


@csrf_exempt
@has_dashboard_permission_required
@login_required
def delete_invoice(request):
    return delete_simple_object(request=request, key='slug', model=Invoice, redirect_url="invoice:create_invoice")


""" 
-------------------------------------------------------------------
                        *** PDF ***
-------------------------------------------------------------------
"""

@method_decorator(login_required, name='dispatch')
class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        # Object
        self.object = get_simple_object(key="slug", model=Invoice, self=self)
        # Company Information
        STATIC_DATA_FILE = os.path.join(settings.BASE_DIR, 'utils/staticData.json')
        # Open and read JSON file
        data_file = open(STATIC_DATA_FILE,)
        data = json.load(data_file)
        comapny_information = data.get("CompanyInformation", {})
        # prepare context data
        context = {
            "object": self.object,
            "company_information": comapny_information,
            "datetime": timezone.now(),
        }
        
        # define required stylesheets
        css =  [
            os.path.join(settings.BASE_DIR, 'staticfiles/admin_panel/assets/css/bootstrap.css'), os.path.join(
                settings.BASE_DIR, 'staticfiles/admin_panel/assets/css/custom.css')
        ]
        
        def create_file_name():
            file_name = '%s Invoice.pdf' % (self.object.get_company())
            return file_name.strip()

        # generate and download PDF
        response = generate_pdf_with_pdfkit(
            template_src="invoice/snippets/invoice-pdf-preview.html",
            context=context,
            css=css,
            filename=create_file_name()
        )
        return response
    
    def dispatch(self, request, *args, **kwargs):
        self.object = get_simple_object(key="slug", model=Invoice, self=self)
        is_superuser = request.user.is_superuser
        is_company = True if self.object.service.filter(
            company__user=request.user).exists() else False
        if not is_superuser and not is_company:
            messages.error(
                self.request, 'Access Denied!'
            )
            return HttpResponseRedirect(reverse('home'))
        return super(GeneratePdf, self).dispatch(request, *args, **kwargs)
    
    
""" 
-------------------------------------------------------------------
                    *** Company Invoice List ***
-------------------------------------------------------------------
"""


@method_decorator(login_required, name='dispatch')
class CompanyInvoiceListView(ListView):
    template_name = "invoice/company-invoice-list.html"
    
    def get_queryset(self):
        qs = None
        company_qs = Company.objects.filter(user=self.request.user)
        if company_qs:
            company = company_qs.first()
            qs = Invoice.objects.filter(service__company=company)
            
        return qs
    
    def dispatch(self, request, *args, **kwargs):
        is_superuser = request.user.is_superuser
        is_company = True if self.request.user.is_company else False
        if not is_superuser and not is_company:
            messages.error(
                self.request, 'Access Denied!'
            )
            return HttpResponseRedirect(reverse('home'))
        return super(CompanyInvoiceListView, self).dispatch(request, *args, **kwargs)
    
    
    def get_context_data(self, **kwargs):
        context = super(
            CompanyInvoiceListView, self
        ).get_context_data(**kwargs)
        context['page_title'] = 'Invoice List'
        context['page_short_title'] = 'Invoice List'
        context['display_name'] = 'Invoice List'
        context['can_view'] = True
        return context
