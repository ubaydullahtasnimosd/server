from django.urls import path
from .import views

urlpatterns = [
    path('', views.BookListCreateView.as_view(), name='book-list-create'),
    path('/<uuid:id>', views.BookRetrieveUpdateDestroyView.as_view(), name='book-retrieve-update-destory')
]