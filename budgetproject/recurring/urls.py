from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.recurring_register, name='recurring_register'),
    path('<uuid:pk>/edit/', views.recurring_edit, name='recurring_edit'),
    path('<uuid:pk>/delete/', views.recurring_delete, name='recurring_delete'),
]