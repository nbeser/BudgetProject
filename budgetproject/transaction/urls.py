from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.transaction_register, name='transaction_register'),
    path('<uuid:pk>/edit/', views.transaction_edit, name='transaction_edit'),
    path('<uuid:pk>/delete/', views.transaction_delete, name='transaction_delete'),
]