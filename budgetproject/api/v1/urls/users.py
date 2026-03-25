from django.urls import path
from api.v1.views.users import SignUpView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
]