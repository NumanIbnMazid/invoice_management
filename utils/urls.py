from django.urls import path
from .views import (
    DashboardSettingView
)


urlpatterns = [
    path('dashboard-setting/', DashboardSettingView.as_view(), name="dashboard_setting"),
]
