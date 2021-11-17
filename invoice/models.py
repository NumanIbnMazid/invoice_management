from django.db import models
from utils.snippets import autoslugWithFieldAndUUID, autoslugFromUUID
from service.models import Service
from deals.models import Coupon, Vat
from django.utils.translation import gettext_lazy as _


@autoslugFromUUID()
class Invoice(models.Model):
    class Status(models.IntegerChoices):
        CANCELLED = 0, _("Cancelled")
        PAID = 1, _("Paid")
        PENDING = 2, _("Pending")
        
    service = models.ManyToManyField(Service, related_name="service_invoices")
    slug = models.SlugField(unique=True, max_length=254)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, related_name='coupon_invoices', null=True, blank=True)
    vat = models.ForeignKey(Vat, on_delete=models.SET_NULL, related_name='vat_invoices', blank=True, null=True)
    additional_charge = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def _get_total_cost(self):
        "Returns the total cost of invoice."
        total = 0
        try:
            for service in self.service.all():
                total += service.price
            # calculate vat
            if self.vat:
                total = total + (total * (self.vat.vat_percentage / 100))
            # calculate coupon
            if self.coupon:
                total = total - self.coupon.discount_amount
            # calculate additional charge
            if self.additional_charge:
                total = total + self.additional_charge
        except Exception as E:
            print(f"*** Total Cost Error: {str(E)} ***")
            
        return round(total, 2)
    # calculated field
    total_cost = property(_get_total_cost)
    
    status = models.PositiveSmallIntegerField(choices=Status.choices, default=Status.PENDING)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'
        ordering = ["-created_at"]

    def __str__(self):
        return ", ".join([service.name + f" ({service.price})" for service in self.service.all()])
    
    def get_status_str(self):
        if self.status == 0:
            return "Cancelled"
        elif self.status == 1:
            return "Paid"
        else:
            return "Pending"

    def get_fields(self):
        def get_dynamic_fields(field):
            if field.name == 'service':
                return (field.name, self.__str__(), field.get_internal_type())
            elif field.name == 'coupon':
                return (field.name, self.coupon.discount_amount, field.get_internal_type())
            elif field.name == 'vat':
                return (field.name, self.vat.vat_percentage, field.get_internal_type())
            else:
                return (field.name, field.value_from_object(self), field.get_internal_type())
        return [get_dynamic_fields(field) for field in (self.__class__._meta.fields + self.__class__._meta.many_to_many)]
