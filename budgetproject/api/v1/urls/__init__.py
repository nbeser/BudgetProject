from django.urls import path, include

urlpatterns = [
    path("users/", include("api.v1.urls.users")),
    path("categories/", include("api.v1.urls.categories")),
    path("transactions/", include("api.v1.urls.transactions")),
]