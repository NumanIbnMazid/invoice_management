from django.urls import path
from .views import (
    CouponCreateView, CouponUpdateView, CouponDetailView, delete_coupon,
    VatCreateView, VatUpdateView, VatDetailView, delete_vat
)

urlpatterns = [
    # ==============================*** Coupon URLS ***==============================
    path("coupon/create/", CouponCreateView.as_view(), name="create_coupon"),
    path("coupon/update/<slug>/", CouponUpdateView.as_view(), name="update_coupon"),
    path("coupon/<slug>/detail/", CouponDetailView.as_view(), name="coupon_detail"),
    path("coupon/delete/", delete_coupon, name="delete_coupon"),
    # ==============================*** Vat URLS ***==============================
    path("vat/create/", VatCreateView.as_view(), name="create_vat"),
    path("vat/update/<slug>/", VatUpdateView.as_view(), name="update_vat"),
    path("vat/<slug>/detail/", VatDetailView.as_view(), name="vat_detail"),
    path("vat/delete/", delete_vat, name="delete_vat"),
]