from rest_framework import serializers
from .models import Comment
from book .models import Book
from Articles_Essays .models import Articles_Essays
from django.contrib.contenttypes.models import ContentType

class CommentSerializers(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    content_object = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'userName', 'userMessage', 'commentCreateAt', 'parent_comment', 'replies', 'content_object']
        read_only_fields = ['commentCreateAt']

    def get_replies(self, obj):
        if hasattr(obj, 'replies'):
            replies = obj.replies.all()
        else:
            replies = Comment.objects.filter(parent_comment=obj)
        serializer = CommentSerializers(replies, many=True, context=self.context)
        return serializer.data
    
    def get_content_object(self, obj):
        if obj.content_type.model == 'book':
            book = Book.objects.get(id=obj.object_id)
            return {'type': 'book', 'id': str(book.id), 'title': book.bookTitle}
        elif obj.content_type.model == 'articles_essays':
            article = Articles_Essays.objects.get(id=obj.object_id)
            return {'type': 'article', 'id': str(article.id), 'title': article.articlesEssaysName}
        return None
        
class CreateCommentSerializer(serializers.ModelSerializer):
    content_type = serializers.CharField(write_only=True, required=True)
    object_id = serializers.UUIDField(write_only=True, required=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'userName', 'userMessage', 'parent_comment', 'content_type', 'object_id']
        read_only_fields = ['id']

    def validate(self, data):
        try:
            content_type = ContentType.objects.get(model=data['content_type'])
        except ContentType.DoesNotExist:
            raise serializers.ValidationError({'content_type': 'Invalid content type'})
        
        model_class = content_type.model_class()
        if not model_class.objects.filter(id=data['object_id']).exists():
            raise serializers.ValidationError({'object_id': 'Object with this ID does not exist'})
        
        return data

    def create(self, validated_data):
        content_type = ContentType.objects.get(model=validated_data.pop('content_type'))
        object_id = validated_data.pop('object_id')
        
        comment = Comment.objects.create(
            content_type=content_type,
            object_id=object_id,
            **validated_data
        )
        return comment