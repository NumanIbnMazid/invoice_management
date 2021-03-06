from django.db import models
from utils.snippets import autoslugWithFieldAndUUID, autoslugFromUUID
from django.core.validators import MaxValueValidator, MinValueValidator
from utils.choices import Currency


@autoslugWithFieldAndUUID(fieldname="code")
class Coupon(models.Model):
    code = models.CharField(max_length=254, unique=True)
    slug = models.SlugField(unique=True, max_length=254)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, choices=Currency.choices, default=Currency.BDT)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Coupon'
        verbose_name_plural = 'Coupons'
        ordering = ["-created_at"]

    def __str__(self):
        return self.code + f" ({str(self.discount_amount)} {self.currency})"
    
    def get_fields(self):
        def get_dynamic_fields(field):
            if field.name == 'discount_amount':
                return (field.name, str(self.discount_amount) + f" {self.currency}", field.get_internal_type())
            else:
                return (field.name, field.value_from_object(self), field.get_internal_type())
        return [get_dynamic_fields(field) for field in self.__class__._meta.fields]


@autoslugFromUUID()
class Vat(models.Model):
    slug = models.SlugField(unique=True, max_length=254)
    vat_percentage = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[
            MaxValueValidator(100),
            MinValueValidator(0.1)
        ]
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Vat'
        verbose_name_plural = 'Vats'
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.vat_percentage) + "%"
    
    def get_fields(self):
        def get_dynamic_fields(field):
            if field.name == 'vat_percentage':
                return (field.name, str(self.vat_percentage) + "%", field.get_internal_type())
            else:
                return (field.name, field.value_from_object(self), field.get_internal_type())
        return [get_dynamic_fields(field) for field in self.__class__._meta.fields]
