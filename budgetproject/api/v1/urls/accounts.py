from django.urls import path
from api.v1.views.accounts import AccountListView, AccountsByUser, AccountDetailView

urlpatterns = [
    path("admin/", AccountListView.as_view(), name="account_list_view"),
    path("", AccountsByUser.as_view(), name="account_by_user"),
    path("<int:pk>/", AccountDetailView.as_view(), name="account_detail_view"),
]