from rest_framework import serializers
from .models import Comment

class CommentSerializers(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'userName', 'userEmail', 'userImage', 'userMessage', 'commentCreateAt', 'parent_comment', 'replies']
        read_only_fields = ['commentCreateAt']

    def get_replies(self, obj):
        if hasattr(obj, 'replies'):
            replies = obj.replies.all()
        else:
            replies = Comment.objects.filter(parent_comment=obj)
        serializer = CommentSerializers(replies, many=True, context=self.context)
        return serializer.data
        
class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['userName', 'userEmail', 'userImage', 'userMessage', 'parent_comment']

    def validate_parent_comment(self, value):
        if value and value.parent_comment:
            raise serializers.ValidationError('You can only reply to top-level comments.')
        return value