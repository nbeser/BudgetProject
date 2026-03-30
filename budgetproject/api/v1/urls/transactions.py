from django.urls import path
from api.v1.views.transactions import TransactionListView, TransactionByUser, TransactionDetailView

urlpatterns = [
    path("admin/", TransactionListView.as_view(), name="transaction_list_view"),
    path("", TransactionByUser.as_view(), name="transaction_by_user"),
    path("<uuid:pk>/", TransactionDetailView.as_view(), name="transaction_detail_view"),
]