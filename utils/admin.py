from django.contrib import admin
from .models import DashboardSetting


class DashboardSettingAdmin(admin.ModelAdmin):
    list_display = ['title', 'skin', 'menu_collapsed', 'layout_width', 'navbar_color', 'navbar_type', 'footer_type', 'created_at', 'updated_at']

    class Meta:
        model = DashboardSetting

admin.site.register(DashboardSetting, DashboardSettingAdmin)
