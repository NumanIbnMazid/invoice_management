from django.views.generic import CreateView, UpdateView, DetailView, ListView
from utils.decorators import has_payment_permission, has_dashboard_permission_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.contrib import messages
from utils.helpers import (
    get_simple_context_data, get_simple_object, delete_simple_object
)
from django.http import HttpResponseRedirect
# App Imports
from .forms import CardManageForm
from .models import Card


card_decorators = [has_payment_permission]
dashboard_decorators = [login_required, has_dashboard_permission_required]

""" 
-------------------------------------------------------------------
                           ** Card ***
-------------------------------------------------------------------
"""


def get_card_common_contexts(request):
    list_objects = Card.objects.filter(user=request.user)
    common_contexts = get_simple_context_data(
        request=request, app_namespace='cards', model_namespace="card", model=Card, list_template=None, fields_to_hide_in_table=["id", "slug","updated_at"]
    )
    common_contexts.update({"list_objects": list_objects})
    return common_contexts


@method_decorator(card_decorators, name='dispatch')
class CardCreateView(CreateView):
    template_name = "admin_panel/snippets/manage.html"
    form_class = CardManageForm

    def form_valid(self, form, **kwargs):
        # Get form values
        user = self.request.user
        # assing user
        form.instance.user = user
        
        if form.is_valid():
            messages.success(
                self.request, 'Created successfully!'
            )
            return super().form_valid(form)
        messages.error(
            self.request, 'Failed to create!'
        )
        return super().form_invalid(form)
    
    def get_form_kwargs(self):
        kwargs = super(CardCreateView, self).get_form_kwargs()
        if self.form_class:
            kwargs.update({'request': self.request})
        return kwargs

    def get_success_url(self):
        return reverse("cards:create_card")

    def get_context_data(self, **kwargs):
        context = super(
            CardCreateView, self
        ).get_context_data(**kwargs)
        context['page_title'] = 'Create Card'
        context['page_short_title'] = 'Create Card'
        for key, value in get_card_common_contexts(request=self.request).items():
            context[key] = value
        return context


@method_decorator(card_decorators, name='dispatch')
class CardDetailView(DetailView):
    template_name = "admin_panel/snippets/detail-common.html"

    def get_object(self):
        return get_simple_object(key='slug', model=Card, self=self)

    def get_context_data(self, **kwargs):
        context = super(
            CardDetailView, self
        ).get_context_data(**kwargs)
        context['page_title'] = 'Card Detail'
        context['page_short_title'] = 'Card Detail'
        for key, value in get_card_common_contexts(request=self.request).items():
            context[key] = value
        return context
    
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        is_superuser = request.user.is_superuser
        is_users_card = True if self.object.user == self.request.user else False
        if not is_superuser and not is_users_card:
            messages.error(
                self.request, 'Access Denied!'
            )
            return HttpResponseRedirect(reverse('home'))
        return super(CardDetailView, self).dispatch(request, *args, **kwargs)


@method_decorator(card_decorators, name='dispatch')
class CardUpdateView(UpdateView):
    template_name = 'admin_panel/snippets/manage.html'
    form_class = CardManageForm

    def get_object(self):
        return get_simple_object(key="slug", model=Card, self=self)

    def get_success_url(self):
        return reverse("cards:create_card")
    
    def get_form_kwargs(self):
        kwargs = super(CardUpdateView, self).get_form_kwargs()
        if self.form_class:
            kwargs.update({'request': self.request})
        return kwargs

    def form_valid(self, form):
        messages.success(
            self.request, 'Updated successfully!'
        )
        return super().form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        is_superuser = request.user.is_superuser
        is_users_card = True if self.object.user == self.request.user else False
        if not is_superuser and not is_users_card:
            messages.error(
                self.request, 'Access Denied!'
            )
            return HttpResponseRedirect(reverse('home'))
        return super(CardUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(
            CardUpdateView, self
        ).get_context_data(**kwargs)
        context['page_title'] = 'Update Card'
        context['page_short_title'] = 'Update Card'
        for key, value in get_card_common_contexts(request=self.request).items():
            context[key] = value
        return context


@csrf_exempt
@login_required
def delete_card(request):
    return delete_simple_object(request=request, key='slug', model=Card, redirect_url="cards:create_card")


@method_decorator(dashboard_decorators, name='dispatch')
class CardListView(ListView):
    template_name = "admin_panel/snippets/list-common.html"
    
    def get_queryset(self):
        return Card.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super(
            CardListView, self
        ).get_context_data(**kwargs)
        context['page_title'] = 'Card List'
        context['page_short_title'] = 'Card List'
        context['display_name'] = 'Card List'
        context['can_view'] = True
        context["list_objects"] = self.get_queryset()
        # models fields
        MODEL_FIELDS = Card._meta.fields
        MODEL_MANY_TO_FIELDS = Card._meta.many_to_many
        context["fields_count"] = len(MODEL_FIELDS)
        context["fields"] = dict(
            [(f.name, f.verbose_name) for f in MODEL_FIELDS + MODEL_MANY_TO_FIELDS]
        )
        context["fields_to_hide_in_table"] = ["id", "slug", "updated_at"]
        return context