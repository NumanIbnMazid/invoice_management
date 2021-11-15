from django.urls import path
from .views import CompanyCreateView, ComapnyUpdateView, CompanyDetailView, delete_company

urlpatterns = [
    # ==============================*** Company URLS ***==============================
    path("create/", CompanyCreateView.as_view(), name="create_company"),
    path("update/<slug>/", ComapnyUpdateView.as_view(), name="update_company"),
    path("<slug>/detail/", CompanyDetailView.as_view(), name="company_detail"),
    path("delete/", delete_company, name="delete_company"),
]
