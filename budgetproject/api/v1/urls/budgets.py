from django.urls import path
from api.v1.views.budgets import BudgetListCreateView, BudgetDetailView

urlpatterns = [
    path("", BudgetListCreateView.as_view(), name="budget_list_create"),
    path("<int:pk>/", BudgetDetailView.as_view(), name="budget_detail"),
]