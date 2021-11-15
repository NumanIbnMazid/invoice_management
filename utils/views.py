from .models import DashboardSetting
from django.http import JsonResponse
from django.views.generic import View
import json
from django.utils import timezone
from .decorators import has_dashboard_permission_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


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
