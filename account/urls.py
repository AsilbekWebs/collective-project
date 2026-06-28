from django.urls import path
<<<<<<< HEAD
from .views import *

urlpatterns = [
    path('signup', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('update', UserUpdateView.as_view(), name='update'),
    path('add-product/', AddProductView.as_view(), name='add_product'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
=======
from django.contrib.auth.views import LogoutView
from .views import UserLoginView, signup

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("signup/", signup, name="signup"),
    path("logout/", LogoutView.as_view(), name="logout"),
>>>>>>> 0830305dc5e2f4f97955ec98c19f2f2cdf9850d2
]