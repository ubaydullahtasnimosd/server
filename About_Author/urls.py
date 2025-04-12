from django.urls import path
from .import views

urlpatterns = [
    path('', views.AboutAuthorApiView.as_view(), name='about-author')
]
