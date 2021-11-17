from django.views.generic import CreateView, UpdateView, DetailView
from utils.decorators import has_dashboard_permission_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.contrib import messages
from utils.helpers import (
    validate_normal_form, get_simple_context_data, get_simple_object, delete_simple_object, user_has_permission
)
# App Imports
from .forms import CouponManageForm, VatManageForm
from .models import Coupon, Vat


dashboard_decorators = [login_required, has_dashboard_permission_required]


""" 
-------------------------------------------------------------------
                        *** Coupon ***
-------------------------------------------------------------------
"""


def get_coupon_common_contexts(request):
    common_contexts = get_simple_context_data(
        request=request, app_namespace='deals', model_namespace="coupon", model=Coupon, list_template=None, fields_to_hide_in_table=["id", "slug", "updated_at"]
    )
    return common_contexts


@method_decorator(dashboard_decorators, name='dispatch')
class CouponCreateView(CreateView):
    template_name = "admin_panel/snippets/manage.html"
    form_class = CouponManageForm

    def form_valid(self, form, **kwargs):
        messages.success(
            self.request, 'Coupon created successfully!'
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("deals:create_coupon")

    def get_context_data(self, **kwargs):
        context = super(
            CouponCreateView, self
        ).get_context_data(**kwargs)
        context['page_title'] = 'Create Coupon'
        context['page_short_title'] = 'Create Coupon'
        for key, value in get_coupon_common_contexts(request=self.request).items():
            context[key] = value
        return context


@method_decorator(dashboard_decorators, name='dispatch')
class CouponDetailView(DetailView):
    template_name = "admin_panel/snippets/detail-common.html"

    def get_object(self):
        return get_simple_object(key='slug', model=Coupon, self=self)

    def get_context_data(self, **kwargs):
        context = super(
            CouponDetailView, self
        ).get_context_data(**kwargs)
        context['page_title'] = f'Coupon - {self.get_object().code} Detail'
        context['page_short_title'] = f'Coupon - {self.get_object().code} Detail'
        for key, value in get_coupon_common_contexts(request=self.request).items():
            context[key] = value
        return context


@method_decorator(dashboard_decorators, name='dispatch')
class CouponUpdateView(UpdateView):
    template_name = 'admin_panel/snippets/manage.html'
    form_class = CouponManageForm

    def get_object(self):
        return get_simple_object(key="slug", model=Coupon, self=self)

    def get_success_url(self):
        return reverse("deals:create_coupon")

    def form_valid(self, form):
        messages.success(
            self.request, 'Coupon updated successfully!'
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(
            CouponUpdateView, self
        ).get_context_data(**kwargs)
        context['page_title'] = f'Update Coupon "{self.get_object().code}"'
        context['page_short_title'] = f'Update Coupon "{self.get_object().code}"'
        for key, value in get_coupon_common_contexts(request=self.request).items():
            context[key] = value
        return context


@csrf_exempt
@has_dashboard_permission_required
@login_required
def delete_coupon(request):
    return delete_simple_object(request=request, key='slug', model=Coupon, redirect_url="deals:create_coupon")


""" 
-------------------------------------------------------------------
                        *** Vat ***
-------------------------------------------------------------------
"""


def get_vat_common_contexts(request):
    # Hide Create Option if vat already exists
    extra_kwargs = {}
    if len(Vat.objects.all()) >= 1:
        extra_kwargs["create_url"] = None
        
    common_contexts = get_simple_context_data(
        request=request, app_namespace='deals', model_namespace="vat", model=Vat, list_template=None, fields_to_hide_in_table=["id", "slug", "updated_at"], **extra_kwargs
    )
    return common_contexts


@method_decorator(dashboard_decorators, name='dispatch')
class VatCreateView(CreateView):
    template_name = "admin_panel/snippets/manage.html"
    form_class = VatManageForm

    def form_valid(self, form, **kwargs):
        messages.success(
            self.request, 'Vat created successfully!'
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("deals:create_vat")

    def get_context_data(self, **kwargs):
        context = super(
            VatCreateView, self
        ).get_context_data(**kwargs)
        context['page_title'] = 'Create Vat'
        context['page_short_title'] = 'Create Vat'
        for key, value in get_vat_common_contexts(request=self.request).items():
            context[key] = value
        
        return context


@method_decorator(dashboard_decorators, name='dispatch')
class VatDetailView(DetailView):
    template_name = "admin_panel/snippets/detail-common.html"

    def get_object(self):
        return get_simple_object(key='slug', model=Vat, self=self)

    def get_context_data(self, **kwargs):
        context = super(
            VatDetailView, self
        ).get_context_data(**kwargs)
        context['page_title'] = f'Vat - {self.get_object().slug} Detail'
        context['page_short_title'] = f'Vat - {self.get_object().slug} Detail'
        for key, value in get_vat_common_contexts(request=self.request).items():
            context[key] = value
        return context


@method_decorator(dashboard_decorators, name='dispatch')
class VatUpdateView(UpdateView):
    template_name = 'admin_panel/snippets/manage.html'
    form_class = VatManageForm

    def get_object(self):
        return get_simple_object(key="slug", model=Vat, self=self)

    def get_success_url(self):
        return reverse("deals:create_vat")

    def form_valid(self, form):
        messages.success(
            self.request, 'Vat updated successfully!'
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(
            VatUpdateView, self
        ).get_context_data(**kwargs)
        context['page_title'] = f'Update Vat "{self.get_object().slug}"'
        context['page_short_title'] = f'Update Vat "{self.get_object().slug}"'
        for key, value in get_vat_common_contexts(request=self.request).items():
            context[key] = value
        return context


@csrf_exempt
@has_dashboard_permission_required
@login_required
def delete_vat(request):
    return delete_simple_object(request=request, key='slug', model=Vat, redirect_url="deals:create_vat")
