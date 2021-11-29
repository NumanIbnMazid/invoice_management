from django.views.generic import TemplateView
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.template import loader
import sys
from django import http
from django.template import Context

class HomepageView(TemplateView):
    template_name = 'user_panel/pages/index.html'


def server_error(request, template_name='handlers/500.html'):
    """
    500 error handler.

    Templates: `500.html`
    Context: sys.exc_info() results
     """
    t = loader.get_template(template_name) # You need to create a 500.html template.
    ltype,lvalue,ltraceback = sys.exc_info()
    sys.exc_clear() #for fun, and to point out I only -think- this hasn't happened at 
                    #this point in the process already
    return http.HttpResponseServerError(t.render(Context({'type':ltype,'value':lvalue,'traceback':ltraceback})))