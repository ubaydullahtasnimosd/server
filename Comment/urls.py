from django.urls import path
from .import views

urlpatterns = [
    path('comments/', views.CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<uuid:id>/', views.CommentDetailView.as_view(), name='comment-detail'),
    path('content/<str:content_type>/<uuid:object_id>/comments/', views.ContentCommentsView.as_view(), name='content-comments'),
]