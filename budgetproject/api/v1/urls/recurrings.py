from django.urls import path
from api.v1.views.recurrings import RecurringListView, RecurringByUser, RecurringDetailView

urlpatterns = [
    path("admin/", RecurringListView.as_view(), name="recurring_list_view"),
    path("", RecurringByUser.as_view(), name="recurring_by_user"),
    path("<uuid:pk>/", RecurringDetailView.as_view(), name="recurring_detail_view"),
]