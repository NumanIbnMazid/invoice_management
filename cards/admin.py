from django.contrib import admin
from utils.mixins import CustomModelAdminMixin
from .models import Card


class CardAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

    class Meta:
        model = Card

admin.site.register(Card, CardAdmin)