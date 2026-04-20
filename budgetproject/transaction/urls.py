from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.transaction_register, name='transaction_register'),
    # path('<int:id>/edit/', views.transaction_edit, name='transaction_edit'),
    # path('<int:id>/delete/', views.transaction_delete, name='transaction_delete'),
]