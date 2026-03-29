from django.urls import path
from api.v1.views.categories import CategoryListView, CategoryListCreateView

urlpatterns = [
    path("admin/", CategoryListView.as_view(), name="category_list_view"),
    path("", CategoryListCreateView.as_view(), name="category_list_create"),
]