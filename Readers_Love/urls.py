from django.urls import path
from .import views

urlpatterns = [
    path('', views.ReadersLoveListView.as_view(), name='readers-love-list'),
    path('image/', views.ReadersLoveImageView.as_view(), name='readers-love-images'),
]