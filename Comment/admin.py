from django.contrib import admin
from .models import Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'userName', 'userMessage', 'commentCreateAt', 'parent_comment']
    list_filter = ['commentCreateAt']
    search_fields = ['userName', 'userMessage']
    readonly_fields = ['commentCreateAt']

admin.site.register(Comment, CommentAdmin)