from rest_framework import generics, permissions
from .models import Comment
from .serializers import CreateCommentSerializer, CommentSerializers
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.filter(parent_comment__isnull=True)
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateCommentSerializer
        return CommentSerializers
    
    def get_queryset(self):
        queryset = super().get_queryset()
        content_type = self.request.query_params.get('content_type')
        object_id = self.request.query_params.get('object_id')
        
        if content_type and object_id:
            try:
                content_type = ContentType.objects.get(model=content_type)
                queryset = queryset.filter(content_type=content_type, object_id=object_id)
            except:
                pass
        return queryset

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers
    permission_classes = [permissions.AllowAny]
    lookup_field = 'id'

class ContentCommentsView(generics.ListAPIView):
    serializer_class = CommentSerializers
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        content_type = self.kwargs.get('content_type')
        object_id = self.kwargs.get('object_id')
        
        content_type = get_object_or_404(ContentType, model=content_type)
        return Comment.objects.filter(
            content_type=content_type,
            object_id=object_id,
            parent_comment__isnull=True
        )