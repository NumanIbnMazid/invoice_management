from django.views.generic import TemplateView

class DashboardView(TemplateView):
    template_name = "admin_panel/pages/index.html"