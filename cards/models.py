from django.db import models
from django.utils.translation import gettext_lazy as _
from utils.snippets import autoslugFromUUID
from django.contrib.auth import get_user_model
from middlewares.request_middleware import RequestMiddleware


@autoslugFromUUID()
class Card(models.Model):
    class CardType(models.TextChoices):
        CREDIT = 'Credit Card', _('Credit Card')
        DEBIT = 'Debit Card', _('Debit Card')
        CHARGE = 'Charge Card', _('Charge Card')
        ATM = 'ATM Card', _('ATM Card')
        STORED_VALUE = 'Stored Value Card', _('Stored Value Card')
        FLEET = 'Fleet Card', _('Fleet Card')
        AMEX = 'Amex Card', _('Amex Card')
        OTHER = 'Other', _('Other')

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='user_cards')
    card_type = models.CharField(max_length=50, choices=CardType.choices, default="Credit Card")
    slug = models.SlugField(unique=True, max_length=254)
    company_name = models.CharField(max_length=200, blank=True, null=True)
    name_on_card = models.CharField(max_length=254)
    card_number = models.PositiveBigIntegerField()
    cvc = models.PositiveIntegerField()
    expire_date = models.DateField()
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    save_card = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="submitted at")
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Card'
        verbose_name_plural = 'Cards'
        ordering = ["-created_at"]

    def __str__(self):
        return self.user.get_dynamic_username() + "'s " + self.card_type

    def get_fields(self):
        def get_dynamic_fields(field):
            request = RequestMiddleware(get_response=None)
            request = request.thread_local.current_request
            if field.name == 'user':
                return (field.name, self.user.get_dynamic_username(), field.get_internal_type())
            elif field.name in ['name_on_card', 'card_number', 'cvc', 'expire_date'] and not request.user.is_staff:
                return (field.name, "*******", field.get_internal_type())
            else:
                return (field.name, field.value_from_object(self), field.get_internal_type())
        return [get_dynamic_fields(field) for field in self.__class__._meta.fields]
