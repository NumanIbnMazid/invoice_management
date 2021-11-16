from django.shortcuts import render
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
from .forms import ServiceManageForm
from .models import Service


dashboard_decorators = [login_required, has_dashboard_permission_required]


""" 
-------------------------------------------------------------------
                        *** Service ***
-------------------------------------------------------------------
"""


def get_service_common_contexts(request):
    common_contexts = get_simple_context_data(
        request=request, app_namespace='service', model_namespace="service", model=Service, list_template=None, fields_to_hide_in_table=["id", "slug", "updated_at"]
    )
    return common_contexts


@method_decorator(dashboard_decorators, name='dispatch')
class ServiceCreateView(CreateView):
    template_name = "admin_panel/snippets/manage.html"
    form_class = ServiceManageForm

    def form_valid(self, form, **kwargs):
        # Get form values
        name = form.instance.name
        company = form.instance.company

        field_qs = Service.objects.filter(
            name__iexact=name, company=company
        )
        result = validate_normal_form(
            field='name', field_qs=field_qs,
            form=form, request=self.request
        )
        if result == 1:
            return super().form_valid(form)
        else:
            return super().form_invalid(form)

    def get_success_url(self):
        return reverse("service:create_service")

    def get_context_data(self, **kwargs):
        context = super(
            ServiceCreateView, self
        ).get_context_data(**kwargs)
        context['page_title'] = 'Create Service'
        context['page_short_title'] = 'Create Service'
        for key, value in get_service_common_contexts(request=self.request).items():
            context[key] = value
        return context


@method_decorator(dashboard_decorators, name='dispatch')
class ServiceDetailView(DetailView):
    template_name = "admin_panel/snippets/detail-common.html"

    def get_object(self):
        return get_simple_object(key='slug', model=Service, self=self)

    def get_context_data(self, **kwargs):
        context = super(
            ServiceDetailView, self
        ).get_context_data(**kwargs)
        context['page_title'] = f'Service - {self.get_object().name} Detail'
        context['page_short_title'] = f'Service - {self.get_object().name} Detail'
        for key, value in get_service_common_contexts(request=self.request).items():
            context[key] = value
        return context


@method_decorator(dashboard_decorators, name='dispatch')
class ServiceUpdateView(UpdateView):
    template_name = 'admin_panel/snippets/manage.html'
    form_class = ServiceManageForm

    def get_object(self):
        return get_simple_object(key="slug", model=Service, self=self)

    def get_success_url(self):
        return reverse("service:create_service")

    def form_valid(self, form):
        self.object = self.get_object()
        name = form.instance.name
        company = form.instance.company

        if not name == self.object.name:
            field_qs = Service.objects.filter(
                name__iexact=name, company=company
            )
            result = validate_normal_form(
                field='name', field_qs=field_qs,
                form=form, request=self.request
            )
            if result == 1:
                return super().form_valid(form)
            else:
                return super().form_invalid(form)
            
        messages.success(
            self.request, 'Service updated successfully!'
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(
            ServiceUpdateView, self
        ).get_context_data(**kwargs)
        context['page_title'] = f'Update Service "{self.get_object().name}"'
        context['page_short_title'] = f'Update Service "{self.get_object().name}"'
        for key, value in get_service_common_contexts(request=self.request).items():
            context[key] = value
        return context


@csrf_exempt
@has_dashboard_permission_required
@login_required
def delete_service(request):
    return delete_simple_object(request=request, key='slug', model=Service, redirect_url="service:create_service")
