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
from django import forms
from dateutil import parser
from dateutil.relativedelta import relativedelta
import datetime
# App Imports
from .forms import CardManageForm
from .models import Card
from utils.models import Configuration


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
        request=request, app_namespace='cards', model_namespace="card", model=Card, list_template="cards/list.html", create_modal="cards/create-modal.html", fields_to_hide_in_table=["id", "slug", "updated_at", "save_card"], allow_datatable_buttons=False, display_name="Service"
    )
    # Card Types
    card_types = {
        'Credit Card': 'Credit Card',
        'Debit Card': 'Debit Card',
        'Charge Card': 'Charge Card',
        'ATM Card': 'ATM Card',
        'Stored Value Card': 'Stored Value Card',
        'Fleet Card': 'Fleet Card',
        'Amex Card': 'Amex Card',
        'Other': 'Other'
    }
    common_contexts.update(
        {
            "list_objects": list_objects, 
            "delete_url": None,
            "update_url": None,
            "can_add": request.user.payment_permission,
            "card_types": card_types,
            "payment_amount_initial": Configuration.objects.last().payment_amount if len(Configuration.objects.all()) > 0 and Configuration.objects.last().is_active else None,
            "card_page_title": Configuration.objects.last().card_page_title if len(Configuration.objects.all()) > 0 and Configuration.objects.last().is_active else None
        }
    )
    return common_contexts


@method_decorator(card_decorators, name='dispatch')
class CardCreateView(CreateView):
    template_name = "admin_panel/snippets/manage.html"
    form_class = CardManageForm
    
    def post(self, request, *args, **kwargs):
        response = super(CardCreateView, self).get(request, *args, **kwargs)
        
        name_on_card = request.POST.get("payment-card-name")
        card_number = request.POST.get("payment-card-number")
        expiry_date = request.POST.get("expiry-date")
        cvc = request.POST.get("payment-card-back-cvv")
        card_type = request.POST.get("card-type")
        company_name = request.POST.get("company-name")
        try:
            payment_amount = float(request.POST.get("payment-amount"))
        except:
            payment_amount = None
        save_card = request.POST.getlist('save-card')
        
        try:
            # set last day of month
            validated_expiry_date = datetime.datetime.strptime(expiry_date, '%m-%y') + relativedelta(day=31)
        except Exception as E:
            messages.error(
                self.request, 'Invalid date format! Please use MM-YY format. i.e: 12-24'
            )
            return response
        
        try:
            if validated_expiry_date < datetime.datetime.now():
                messages.error(request, "Card expired!")
                return HttpResponseRedirect(reverse('cards:create_card'))
            Card.objects.create(
                name_on_card=name_on_card, card_number=card_number, expire_date=validated_expiry_date, cvc=cvc, card_type=card_type, company_name=company_name, payment_amount=payment_amount, save_card=True, user=self.request.user
            )
            
            # update user payment permssion
            request.user.payment_permission = False
            request.user.save()
            
            messages.success(
                self.request, 'Service payment successfull!'
            )
            return HttpResponseRedirect(reverse('cards:create_card'))
        except Exception as e:
            messages.error(
                self.request, f'Something went wrong! {e}'
            )
            HttpResponseRedirect(reverse('home'))
        
        return response
        
    def get_form_kwargs(self):
        kwargs = super(CardCreateView, self).get_form_kwargs()
        if self.form_class:
            kwargs.update(
                {'request': self.request, "object": None}
            )
        return kwargs

    def get_success_url(self):
        return reverse("cards:create_card")

    def get_context_data(self, **kwargs):
        context = super(
            CardCreateView, self
        ).get_context_data(**kwargs)
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
            kwargs.update(
                {'request': self.request, "object": self.get_object()}
            )
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
        context['page_title'] = 'Service Payment (Card) List'
        context['page_short_title'] = 'Service Payment (Card) List'
        context['display_name'] = 'Service Payment (Card) List'
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