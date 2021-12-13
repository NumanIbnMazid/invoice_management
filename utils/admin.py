from django.contrib import admin
from .models import DashboardSetting, Configuration


class DashboardSettingAdmin(admin.ModelAdmin):
    list_display = ['title', 'skin', 'menu_collapsed', 'layout_width', 'navbar_color', 'navbar_type', 'footer_type', 'created_at', 'updated_at']

    class Meta:
        model = DashboardSetting

admin.site.register(DashboardSetting, DashboardSettingAdmin)


class ConfigurationAdmin(admin.ModelAdmin):
    list_display = ['payment_amount', 'currency', 'is_active', 'created_at', 'updated_at']

    class Meta:
        model = Configuration

admin.site.register(Configuration, ConfigurationAdmin)
