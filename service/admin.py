from django.contrib import admin
from utils.mixins import CustomModelAdminMixin
from .models import Service


class ServiceAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

    class Meta:
        model = Service


admin.site.register(Service, ServiceAdmin)
