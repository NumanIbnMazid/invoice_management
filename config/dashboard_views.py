from django.views.generic import TemplateView
from utils.decorators import has_dashboard_permission_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


dashboard_decorators = [login_required]


@method_decorator(dashboard_decorators, name='dispatch')
class DashboardView(TemplateView):
    template_name = "admin_panel/pages/index.html"