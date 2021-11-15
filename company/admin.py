from django.contrib import admin
from utils.mixins import CustomModelAdminMixin
from .models import Company


class CompanyAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

    class Meta:
        model = Company


admin.site.register(Company, CompanyAdmin)
