from django import template
from utils.models import DashboardSetting


register = template.Library()


@register.simple_tag(name='get_dashboard_setting')
def get_dashboard_setting():
    dashboard_setting_qs = DashboardSetting.objects.all()
    if not dashboard_setting_qs.exists():
        dashboard_setting_instance = DashboardSetting.objects.create(title="Dashboard")
        return dashboard_setting_instance
    else:
        dashboard_setting_instance = dashboard_setting_qs.last()
        return dashboard_setting_instance