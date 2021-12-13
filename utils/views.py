from .models import DashboardSetting, Configuration
from django.http import JsonResponse
from django.views.generic import View
import json
from django.utils import timezone
from .decorators import has_dashboard_permission_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from utils.helpers import (
    validate_normal_form, get_simple_context_data, get_simple_object, delete_simple_object, user_has_permission
)
from django.views.generic import CreateView, UpdateView, DetailView
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.contrib import messages
from .forms import ConfigurationManageForm


dashboard_decorators = [login_required, has_dashboard_permission_required]


""" 
-------------------------------------------------------------------
                        ** Dashboard Setting ***
-------------------------------------------------------------------
"""


@method_decorator(dashboard_decorators, name='dispatch')
class DashboardSettingView(View):

    def post(self, *args, **kwargs):

        if self.request.is_ajax and self.request.method == "POST":
            try:
                # Get Config Values
                dashboard_setting = json.loads(
                    self.request.body).get("setting-object", None)
                """
                Example Request Body Object:
                "setting-object": {
                    key: "skin-config",
                    value: value
                }
                """
                # define available keys
                available_keys = ["skin-config", "menu-collapsed-config", "layout-width-config",
                                  "navbar-color-config", "navbar-type-config", "footer-type-config"]

                # get setting key
                setting_key = dashboard_setting.get("key", [])

                if setting_key in available_keys:
                    # get setting value
                    setting_value = dashboard_setting.get("value", None)

                    # get all objects of DashboardSetting
                    dashboard_setting_qs = DashboardSetting.objects.all()

                    # check if dashboard setting object exists, if not then create a DashboardSetting object
                    if dashboard_setting_qs:
                        pass
                    else:
                        DashboardSetting.objects.create(
                            title="Dashboard"
                        )

                    # update dashboard setting based on setting key
                    if setting_key == "skin-config":
                        dashboard_setting_qs.update(
                            skin=setting_value, updated_at=timezone.now()
                        )
                    elif setting_key == "menu-collapsed-config":
                        dashboard_setting_qs.update(
                            menu_collapsed=setting_value, updated_at=timezone.now()
                        )
                    elif setting_key == "layout-width-config":
                        dashboard_setting_qs.update(
                            layout_width=setting_value, updated_at=timezone.now()
                        )
                    elif setting_key == "navbar-color-config":
                        dashboard_setting_qs.update(
                            navbar_color=setting_value, updated_at=timezone.now()
                        )
                    elif setting_key == "navbar-type-config":
                        dashboard_setting_qs.update(
                            navbar_type=setting_value, updated_at=timezone.now()
                        )
                    elif setting_key == "footer-type-config":
                        dashboard_setting_qs.update(
                            footer_type=setting_value, updated_at=timezone.now()
                        )
                    else:
                        dashboard_setting_qs.update(
                            title="Dashboard", updated_at=timezone.now()
                        )
                else:
                    raise ValueError(
                        f"Invalid key: {setting_key} given! Available keys are {available_keys}"
                    )
                return JsonResponse({"valid": True}, status=200)
            except Exception as E:
                return JsonResponse({"valid": False, "Exception": str(E)}, status=400)
        return JsonResponse({}, status=400)


""" 
-------------------------------------------------------------------
                        ** Configuration ***
-------------------------------------------------------------------
"""


def get_configuration_common_contexts(request):
    # Hide Create Option if vat already exists
    extra_kwargs = {}
    if len(Configuration.objects.all()) >= 1:
        extra_kwargs["create_url"] = None

    common_contexts = get_simple_context_data(
        request=request, app_namespace='utils', model_namespace="configuration", model=Configuration, list_template=None, fields_to_hide_in_table=["id"], **extra_kwargs
    )
    return common_contexts


@method_decorator(dashboard_decorators, name='dispatch')
class ConfigurationCreateView(CreateView):
    template_name = "admin_panel/snippets/manage.html"
    form_class = ConfigurationManageForm

    def form_valid(self, form, **kwargs):
        messages.success(
            self.request, 'Configuration created successfully!'
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("utils:create_configuration")

    def get_context_data(self, **kwargs):
        context = super(
            ConfigurationCreateView, self
        ).get_context_data(**kwargs)
        context['page_title'] = 'Create Configuration'
        context['page_short_title'] = 'Create Configuration'
        for key, value in get_configuration_common_contexts(request=self.request).items():
            context[key] = value
        return context


@method_decorator(dashboard_decorators, name='dispatch')
class ConfigurationDetailView(DetailView):
    template_name = "admin_panel/snippets/detail-common.html"

    def get_object(self):
        return get_simple_object(key='slug', model=Configuration, self=self)

    def get_context_data(self, **kwargs):
        context = super(
            ConfigurationDetailView, self
        ).get_context_data(**kwargs)
        context['page_title'] = 'Configuration Detail'
        context['page_short_title'] = 'Configuration Detail'
        for key, value in get_configuration_common_contexts(request=self.request).items():
            context[key] = value
        return context


@method_decorator(dashboard_decorators, name='dispatch')
class ConfigurationUpdateView(UpdateView):
    template_name = 'admin_panel/snippets/manage.html'
    form_class = ConfigurationManageForm

    def get_object(self):
        return get_simple_object(key="slug", model=Configuration, self=self)

    def get_success_url(self):
        return reverse("utils:create_configuration")

    def form_valid(self, form):
        messages.success(
            self.request, 'Configuration updated successfully!'
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(
            ConfigurationUpdateView, self
        ).get_context_data(**kwargs)
        context['page_title'] = 'Update Configuration'
        context['page_short_title'] = 'Update Configuration'
        for key, value in get_configuration_common_contexts(request=self.request).items():
            context[key] = value
        return context


@csrf_exempt
@has_dashboard_permission_required
@login_required
def delete_configuration(request):
    return delete_simple_object(request=request, key='slug', model=Configuration, redirect_url="utils:create_configuration")
