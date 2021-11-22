from django.urls import path
from .views import InvoiceCreateView, InvoiceUpdateView, InvoiceDetailView, delete_invoice, GeneratePdf

urlpatterns = [
    # ==============================*** Invoice URLS ***==============================
    path("create/", InvoiceCreateView.as_view(), name="create_invoice"),
    path("update/<slug>/", InvoiceUpdateView.as_view(), name="update_invoice"),
    path("<slug>/detail/", InvoiceDetailView.as_view(), name="invoice_detail"),
    path("delete/", delete_invoice, name="delete_invoice"),
    # PDF URLs
    path("<slug>/pdf/", GeneratePdf.as_view(), name="invoice_pdf_download"),
]
