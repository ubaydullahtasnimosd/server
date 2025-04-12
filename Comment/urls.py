from django.urls import path
from .import views

urlpatterns = [
    path('', views.CommentListCreateView.as_view(), name='comment-list-create'),
    path('/<uuid:id>', views.CommentDetailView.as_view(), name='comment-detail'),
]