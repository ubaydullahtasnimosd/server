from django.contrib import admin
from .models import Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'userName', 'userEmail', 'userMessage', 'userImage', 'commentCreateAt', 'parent_comment']
    list_filter = ['commentCreateAt']
    search_fields = ['userName', 'userEmail', 'userMessage']
    readonly_fields = ['commentCreateAt']

admin.site.register(Comment, CommentAdmin)