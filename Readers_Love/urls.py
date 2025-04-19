from django.urls import path
from . import views

urlpatterns = [
    path('readers/', views.ReadersLoveListCreateView.as_view(), name='readers-love-list'),
    path('image/', views.ReadersLoveImgListView.as_view(), name='readers-love-images'),
]