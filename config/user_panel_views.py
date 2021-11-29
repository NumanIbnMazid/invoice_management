from django.views.generic import TemplateView
from django.urls import reverse
from django.http import HttpResponseRedirect

class HomepageView(TemplateView):
    template_name = 'user_panel/pages/index.html'
    
    def get(self, request):
        return HttpResponseRedirect(reverse("dashboard"))
