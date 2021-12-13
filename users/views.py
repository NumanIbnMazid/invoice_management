from django.views.generic import CreateView, DetailView, UpdateView
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
from .forms import UserManageForm, UserUpdateForm
from django.contrib.auth import get_user_model


dashboard_decorators = [login_required, has_dashboard_permission_required]


""" 
-------------------------------------------------------------------
                           ** User ***
-------------------------------------------------------------------
"""


def get_user_common_contexts(request):
    common_contexts = get_simple_context_data(
        request=request, app_namespace='users', model_namespace="user", model=get_user_model(), list_template="users/list.html", fields_to_hide_in_table=["id", "slug", "password", "updated_at", "is_active", "date_joined", "last_login", "groups", "user_permissions"]
    )
    return common_contexts


@method_decorator(dashboard_decorators, name='dispatch')
class UserCreateView(CreateView):
    template_name = "admin_panel/snippets/manage.html"
    form_class = UserManageForm

    def form_valid(self, form, **kwargs):
        # Get form values
        name = form.instance.name
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')

        if form.is_valid():
            try:
                user_obj = User(
                    name=name,
                    email=email
                )
                user_obj.set_password(password)
                user_obj.save()
                messages.success(
                    self.request, 'User created successfully!'
                )
                return super().form_valid(form)

            except Exception as E:
                pass
        messages.error(
            self.request, 'Failed to create user!'
        )
        return super().form_invalid(form)
        

    def get_success_url(self):
        return reverse("users:create_user")

    def get_context_data(self, **kwargs):
        context = super(
            UserCreateView, self
        ).get_context_data(**kwargs)
        context['page_title'] = 'Create User'
        context['page_short_title'] = 'Create User'
        for key, value in get_user_common_contexts(request=self.request).items():
            context[key] = value
        return context


@method_decorator(dashboard_decorators, name='dispatch')
class UserDetailView(DetailView):
    template_name = "admin_panel/snippets/detail-common.html"

    def get_object(self):
        return get_simple_object(key='slug', model=get_user_model(), self=self)

    def get_context_data(self, **kwargs):
        context = super(
            UserDetailView, self
        ).get_context_data(**kwargs)
        context['page_title'] = f'User Detail'
        context['page_short_title'] = f'User Detail'
        for key, value in get_user_common_contexts(request=self.request).items():
            context[key] = value
        return context
    

@method_decorator(dashboard_decorators, name='dispatch')
class UserUpdateView(UpdateView):
    template_name = 'admin_panel/snippets/manage.html'
    form_class = UserUpdateForm

    def get_object(self):
        return get_simple_object(key="slug", model=get_user_model(), self=self)

    def get_success_url(self):
        return reverse("users:create_user")

    def form_valid(self, form):
        messages.success(
            self.request, "User updated successfully!"
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(
            UserUpdateView, self
        ).get_context_data(**kwargs)
        context['page_title'] = 'Update User'
        context['page_short_title'] = 'Update User'
        for key, value in get_user_common_contexts(request=self.request).items():
            context[key] = value
        return context


@csrf_exempt
@has_dashboard_permission_required
@login_required
def delete_user(request):
    return delete_simple_object(request=request, key='slug', model=get_user_model(), redirect_url="users:create_user")
