from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.category_register, name='category_register'),
    path('<int:id>/edit/', views.category_edit, name='category_edit'),
    path('<int:id>/delete/', views.category_delete, name='category_delete'),
]