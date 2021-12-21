from django.urls import path
from .views import CardCreateView, CardUpdateView, CardDetailView, delete_card, CardListView

urlpatterns = [
    # ==============================*** Card URLS ***==============================
    path("create/", CardCreateView.as_view(), name="create_card"),
    # path("update/<slug>/", CardUpdateView.as_view(), name="update_card"),
    path("<slug>/detail/", CardDetailView.as_view(), name="card_detail"),
    # path("delete/", delete_card, name="delete_card"),
    # Card List View for admin usage
    path("list/", CardListView.as_view(), name="admin_card_list"),
]
