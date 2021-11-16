from django.urls import path
from .views import ServiceCreateView, ServiceUpdateView, ServiceDetailView, delete_service

urlpatterns = [
    # ==============================*** Service URLS ***==============================
    path("create/", ServiceCreateView.as_view(), name="create_service"),
    path("update/<slug>/", ServiceUpdateView.as_view(), name="update_service"),
    path("<slug>/detail/", ServiceDetailView.as_view(), name="service_detail"),
    path("delete/", delete_service, name="delete_service"),
]
