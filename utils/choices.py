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
    DOLLAR = "DOLLAR", _("DOLLAR")
    EURO = "EURO", _("EURO")
