from django.urls import path
from api.v1.views.categories import CategoryListView, CategoryListCreateView, CategoryDetailView

urlpatterns = [
    path("admin/", CategoryListView.as_view(), name="category_list_view"),
    path("", CategoryListCreateView.as_view(), name="category_list_create"),
    path("<int:pk>/", CategoryDetailView.as_view(), name="category_detail_view"),
]