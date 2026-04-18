from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from unfold.admin import ModelAdmin

from .models import Comment
from book.models import Book
from Articles_Essays.models import Articles_Essays


@admin.register(Comment)
class CommentAdmin(ModelAdmin):
    list_display = (
        "id",
        "userName",
        "linked_content",
        "is_reply",
        "commentCreateAt",
    )

    search_fields = (
        "userName",
        "userMessage",
    )

    list_filter = (
        "commentCreateAt",
        "content_type",
    )

    ordering = ("-commentCreateAt",)

    list_per_page = 20

    readonly_fields = (
        "commentCreateAt",
    )

    raw_id_fields = (
        "parent_comment",
    )

    fieldsets = (
        ("Comment Information", {
            "fields": (
                "userName",
                "userMessage",
                "parent_comment",
            )
        }),
        ("Linked Content", {
            "fields": (
                "content_type",
                "object_id",
            )
        }),
        ("Timestamp", {
            "fields": (
                "commentCreateAt",
            )
        }),
    )

    def linked_content(self, obj):
        if obj.content_type and obj.object_id:
            try:
                if obj.content_type.model == "book":
                    book = Book.objects.get(id=obj.object_id)
                    return f"Book: {book.bookTitle}"
                elif obj.content_type.model == "articles_essays":
                    article = Articles_Essays.objects.get(id=obj.object_id)
                    return f"Article: {article.articlesEssaysName}"
            except (Book.DoesNotExist, Articles_Essays.DoesNotExist):
                return "Linked object deleted"
        return "Not linked"

    linked_content.short_description = "Linked Content"

    def is_reply(self, obj):
        return bool(obj.parent_comment)

    is_reply.boolean = True
    is_reply.short_description = "Is Reply"

    def save_model(self, request, obj, form, change):
        if not obj.content_type and not obj.object_id:
            book = Book.objects.first()
            if book:
                obj.content_type = ContentType.objects.get_for_model(Book)
                obj.object_id = book.id
        super().save_model(request, obj, form, change)