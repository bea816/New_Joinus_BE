from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),  # 회원가입 경로
    path('username_unique/', UsernameUniqueView.as_view(), name='username_unique'),  # 닉네임 중복 확인 경로
]
