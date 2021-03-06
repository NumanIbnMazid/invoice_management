from django.db import models
from utils.snippets import autoslugWithFieldAndUUID
from company.models import Company
from utils.choices import Currency
from django.db.models.functions import ExtractMonth
from django.utils import timezone
import datetime
from dateutil.relativedelta import relativedelta


@autoslugWithFieldAndUUID(fieldname="name")
class Service(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_services')
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=254)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, choices=Currency.choices, default=Currency.BDT)
    registration_date = models.DateField()
    due_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        ordering = ["-created_at"]

    def __str__(self):
        return self.name + f" ({str(self.price)} {self.currency})"
    
    def get_fields(self):
        def get_dynamic_fields(field):
            if field.name == 'company':
                return (field.name, self.company.name, field.get_internal_type())
            if field.name == 'price':
                return (field.name, str(self.price) + f" {self.currency}", field.get_internal_type())
            else:
                return (field.name, field.value_from_object(self), field.get_internal_type())
        return [get_dynamic_fields(field) for field in self.__class__._meta.fields]
    
    def get_pending_invoice_dates(self):
        dates = []
        start_date = self.created_at
        end_date = timezone.now()
        delta = relativedelta(months=1)

        while start_date <= end_date:
            if not (start_date.month, start_date.year) in self.service_invoices.filter(service__slug__iexact=self.slug).values_list(
                    'created_at__month', 'created_at__year'):
                dates.append(
                    f"* {start_date.strftime('%B %Y')}"
                )
            start_date += delta
            
        if self.is_active == True:
        
            if len(dates) <= 0:
                return "-"
            
            return ", ".join(dates)
        
        return "-"
