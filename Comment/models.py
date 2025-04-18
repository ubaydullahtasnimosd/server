from django.db import models
import uuid

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    userName = models.CharField(max_length=500, verbose_name='কমেন্টকারীর নাম')
    userMessage = models.TextField(verbose_name='কমেন্টকারীর কমেন্ট')
    commentCreateAt = models.DateTimeField(auto_now_add=True, verbose_name='কমেন্টকারী কখন কমেন্টটি করেছে')
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies', verbose_name='যে কমেন্ট করেছে')

    def __str__(self):
        return f'Comment By - {self.userName}'
    
    @property
    def is_reply(self):
        return self.parent_comment is not None
    
    class Meta:
        ordering = ['-commentCreateAt']
        verbose_name_plural = 'কমেন্ট'