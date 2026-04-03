from django.urls import path
from api.v1.views.recurrings import RecurringListView, RecurringByUser

urlpatterns = [
    path("admin/", RecurringListView.as_view(), name="recurring_list_view"),
    path("", RecurringByUser.as_view(), name="recurring_by_user"),
    # path("<uuid:pk>/", TransactionDetailView.as_view(), name="transaction_detail_view"),
]