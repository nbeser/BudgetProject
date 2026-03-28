from django.urls import path
from api.v1.views.categories import CategoryListView, CategoryListByUser

urlpatterns = [
    path("", CategoryListView.as_view(), name="category_list_view"),
    path("user/", CategoryListByUser.as_view(), name="category_list_view"),
]