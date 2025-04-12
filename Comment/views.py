from rest_framework import generics, permissions
from .models import Comment
from .serializers import CreateCommentSerializer, CommentSerializers

class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.filter(parent_comment__isnull=True)
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateCommentSerializer
        return CommentSerializers
    
    def perform_create(self, serializer):
        serializer.save()

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers
    permission_classes = [permissions.AllowAny]
    lookup_field = 'id'  