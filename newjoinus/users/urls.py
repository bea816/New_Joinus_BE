from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'), 
    path('username_unique/', UsernameUniqueView.as_view(), name='username_unique'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('usernameupdate/', UsernameUpdateView.as_view(), name='username-update'),
    path('delete/', UserDeleteAPIView.as_view(), name='user-delete'),
]
