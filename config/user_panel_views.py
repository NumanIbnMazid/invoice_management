from django.views.generic import TemplateView

class HomepageView(TemplateView):
    template_name = 'user_panel/pages/index.html'