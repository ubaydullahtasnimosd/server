from django.db import models
import uuid
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    userName = models.CharField(max_length=500, verbose_name='কমেন্টকারীর নাম')
    userMessage = models.TextField(verbose_name='কমেন্টকারীর কমেন্ট')
    commentCreateAt = models.DateTimeField(auto_now_add=True, verbose_name='কমেন্টকারী কখন কমেন্টটি করেছে')
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies', verbose_name='মূল কমেন্ট')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.UUIDField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f'Comment By - {self.userName}'
    
    @property
    def is_reply(self):
        return self.parent_comment is not None
    
    class Meta:
        ordering = ['-commentCreateAt']
        verbose_name_plural = 'কমেন্ট'