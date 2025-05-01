from django.urls import path
from .views import *

urlpatterns = [
    path('itemlist/', ItemListAPIView.as_view()),
    path('item/<int:pk>/', ItemDetailAPIView.as_view()),
]