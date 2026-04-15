from django.urls import path
from . import views

urlpatterns = [
    path('', views.pages_index, name='pages_index'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('budgets/', views.get_budget, name='get_budget'),
    path('account/<int:id>/', views.accounts, name='accounts_view'),
    path('operations/', views.operations, name='operations'),
]