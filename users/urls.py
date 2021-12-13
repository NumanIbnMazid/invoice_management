from django.urls import path
from .views import UserCreateView, UserDetailView, UserUpdateView, delete_user

urlpatterns = [
    # ==============================*** User URLS ***==============================
    path("create/", UserCreateView.as_view(), name="create_user"),
    path("update/<slug>/", UserUpdateView.as_view(), name="update_user"),
    path("<slug>/detail/", UserDetailView.as_view(), name="user_detail"),
    path("delete/", delete_user, name="delete_user"),
]