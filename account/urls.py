from django.urls import path
from .views import *

urlpatterns = [
    path('signup', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('update', UserUpdateView.as_view(), name='update'),
    path('add-product/', AddProductView.as_view(), name='add_product'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
]