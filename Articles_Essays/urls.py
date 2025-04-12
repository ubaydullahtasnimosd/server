from django.urls import path
from .import views

urlpatterns = [
    path('', views.ArticlesEssaysListCreateView.as_view(), name='articles-essays-list-create'),
    path('/<uuid:id>', views.ArticlesEssaysRetrieveUpdateDestroyView.as_view(), name='articles-essays-retrieve-update-destroy')
]