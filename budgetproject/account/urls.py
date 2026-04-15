from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.account_register, name='account_register'),
    path('<int:id>/edit/', views.account_edit, name='account_edit'),
    path('<int:id>/delete/', views.account_delete, name='account_delete'),
]