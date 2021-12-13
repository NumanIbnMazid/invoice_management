from django.urls import path
from .views import (
    DashboardSettingView,
    ConfigurationCreateView, ConfigurationUpdateView, ConfigurationDetailView, delete_configuration
)


urlpatterns = [
    path('dashboard-setting/', DashboardSettingView.as_view(), name="dashboard_setting"),
    # ==============================*** Configuration URLS ***==============================
    path("configuration/create/", ConfigurationCreateView.as_view(), name="create_configuration"),
    path("configuration/update/<slug>/", ConfigurationUpdateView.as_view(), name="update_configuration"),
    path("configuration/<slug>/detail/", ConfigurationDetailView.as_view(), name="configuration_detail"),
    path("configuration/delete/", delete_configuration, name="delete_configuration"),
]
