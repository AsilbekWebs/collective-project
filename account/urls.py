from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import UserLoginView, signup

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("signup/", signup, name="signup"),
    path("logout/", LogoutView.as_view(), name="logout"),
]