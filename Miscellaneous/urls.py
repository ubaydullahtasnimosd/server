from django.urls import path
from .import views

urlpatterns = [
    path('', views.MisecllaneousApiView.as_view(), name='misecllaneous-list-create'),
]