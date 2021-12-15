from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, UpdateView, DetailView, ListView
from utils.decorators import has_dashboard_permission_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.contrib import messages
from users.models import User
from utils.helpers import (
    validate_normal_form, get_simple_context_data, get_simple_object, delete_simple_object, user_has_permission
)
# App Imports
from .forms import CompanyCreateForm, CompanyManageForm
from .models import Company


dashboard_decorators = [login_required, has_dashboard_permission_required]

""" 
-------------------------------------------------------------------
                           ** Company ***
-------------------------------------------------------------------
"""


def get_company_common_contexts(request):
    common_contexts = get_simple_context_data(
        request=request, app_namespace='company', model_namespace="company", model=Company, list_template=None, fields_to_hide_in_table=["id", "slug", "description", "updated_at"]
    )
    return common_contexts


@method_decorator(dashboard_decorators, name='dispatch')
class CompanyCreateView(CreateView):
    template_name = "admin_panel/snippets/manage.html"
    form_class = CompanyCreateForm

    def form_valid(self, form, **kwargs):
        # Get form values
        name = form.instance.name
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        
        if form.is_valid():
            try:
                user_obj = User(
                    name=name,
                    email=email,
                    is_company=True
                )
                user_obj.set_password(password)
                user_obj.save()
                
                # save company user
                form.instance.user = user_obj

            except Exception as E:
                messages.error(
                    self.request, 'Failed to create user!'
                )
                return super().form_invalid(form)
        
        
        field_qs = Company.objects.filter(
            name__iexact=name
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
        return reverse("company:create_company")

    def get_context_data(self, **kwargs):
        context = super(
            CompanyCreateView, self
        ).get_context_data(**kwargs)
        context['page_title'] = 'Create Company'
        context['page_short_title'] = 'Create Company'
        for key, value in get_company_common_contexts(request=self.request).items():
            context[key] = value
        return context


@method_decorator(dashboard_decorators, name='dispatch')
class CompanyDetailView(DetailView):
    template_name = "admin_panel/snippets/detail-common.html"

    def get_object(self):
        return get_simple_object(key='slug', model=Company, self=self)

    def get_context_data(self, **kwargs):
        context = super(
            CompanyDetailView, self
        ).get_context_data(**kwargs)
        context['page_title'] = f'Comapny - {self.get_object().name} Detail'
        context['page_short_title'] = f'Comapny - {self.get_object().name} Detail'
        for key, value in get_company_common_contexts(request=self.request).items():
            context[key] = value
        return context


@method_decorator(dashboard_decorators, name='dispatch')
class ComapnyUpdateView(UpdateView):
    template_name = 'admin_panel/snippets/manage.html'
    form_class = CompanyManageForm

    def get_object(self):
        return get_simple_object(key="slug", model=Company, self=self)

    def get_success_url(self):
        return reverse("company:create_company")

    def form_valid(self, form):
        self.object = self.get_object()
        name = form.instance.name
        
        field_qs = Company.objects.filter(
            name__iexact=name
        ).exclude(name__iexact=self.object.name)
        result = validate_normal_form(
            field='name', field_qs=field_qs,
            form=form, request=self.request
        )
        if result == 1:
            # update user name to company name
            user_qs = User.objects.filter(email__iexact=self.object.user.email)
            if user_qs and not name == self.object.user.name:
                user_qs.update(name=name)
                
            return super().form_valid(form)
        else:
            return super().form_invalid(form)


    def get_context_data(self, **kwargs):
        context = super(
            ComapnyUpdateView, self
        ).get_context_data(**kwargs)
        context['page_title'] = f'Update Company "{self.get_object().name}"'
        context['page_short_title'] = f'Update Company "{self.get_object().name}"'
        for key, value in get_company_common_contexts(request=self.request).items():
            context[key] = value
        return context


@csrf_exempt
@has_dashboard_permission_required
@login_required
def delete_company(request):
    return delete_simple_object(request=request, key='slug', model=Company, redirect_url="company:create_company")

