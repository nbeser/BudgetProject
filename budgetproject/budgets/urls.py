from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.budget_register, name='budget_register'),
    path('<int:id>/edit/', views.budget_edit, name='budget_edit'),
    # path('<int:id>/delete/', views.account_delete, name='account_delete'),
]