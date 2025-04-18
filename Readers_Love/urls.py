from django.urls import path
from .import views

urlpatterns = [
    path('', views.ReadersLoveApiView.as_view(), name='readers-love-list'),
]