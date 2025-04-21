from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from .models import Comment
from book.models import Book
from Articles_Essays .models import Articles_Essays

class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'userName', 'content_object_display', 'commentCreateAt', 'is_reply']
    list_filter = ['commentCreateAt', 'content_type']
    search_fields = ['userName', 'userMessage']
    readonly_fields = ['commentCreateAt']
    raw_id_fields = ['parent_comment']

    def content_object_display(self, obj):
        if obj.content_type and obj.object_id:
            try:
                if obj.content_type.model == 'book':
                    book = Book.objects.get(id=obj.object_id)
                    return f"Book: {book.bookTitle}"
                elif obj.content_type.model == 'articles_essays':
                    article = Articles_Essays.objects.get(id=obj.object_id)
                    return f"Article: {article.articlesEssaysName}"
            except (Book.DoesNotExist, Articles_Essays.DoesNotExist):
                return "Linked object deleted"
        return "Not linked"
    
    content_object_display.short_description = 'Linked Content'

    def save_model(self, request, obj, form, change):
        if not obj.content_type and not obj.object_id:
            book = Book.objects.first()
            if book:
                obj.content_type = ContentType.objects.get_for_model(Book)
                obj.object_id = book.id
        super().save_model(request, obj, form, change)

admin.site.register(Comment, CommentAdmin)