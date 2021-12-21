from django.db import models
from django.utils.translation import gettext_lazy as _

# BDT = 'BDT'
# DOLLAR = 'DOLLAR'
# EURO = 'EURO'
# CURRENCY_CHOICES = (
#     (BDT, 'BDT'),
#     (DOLLAR, 'DOLLAR'),
#     (EURO, 'EURO')
# )

class Currency(models.TextChoices):
    BDT = "BDT", _("BDT")
    USD = "USD", _("USD")
    EURO = "EURO", _("EURO")
