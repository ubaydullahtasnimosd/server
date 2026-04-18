from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from .models import Book


def get_image_url(image_field):
    if not image_field:
        return None
    try:
        return image_field.url
    except AttributeError:
        return image_field


@admin.register(Book)
class BookAdmin(ModelAdmin):
    list_display = (
        "id",
        "book_image_preview",
        "bookTitle",
        "bookPublication",
        "short_description",
        "bookPurchaseLink",
        "bookCreatedAt",
    )

    search_fields = (
        "bookTitle",
        "bookPublication",
        "bookDescription",
        "bookPurchaseLink",
    )

    list_filter = (
        "bookCreatedAt",
    )

    ordering = ("-bookCreatedAt",)

    list_per_page = 20

    readonly_fields = (
        "bookCreatedAt",
        "bookUpdateAt",
    )

    fieldsets = (
        ("Book Information", {
            "fields": (
                "bookImage",
                "bookTitle",
                "bookPublication",
                "bookDescription",
                "bookPurchaseLink",
            )
        }),
        ("Timestamps", {
            "fields": (
                "bookCreatedAt",
                "bookUpdateAt",
            )
        }),
    )

    def book_image_preview(self, obj):
        image_url = get_image_url(obj.bookImage)
        if not image_url:
            return "-"
        return format_html(
            '<img src="{}" width="60" height="60" style="border-radius:6px; object-fit:cover;" />',
            image_url
        )

    book_image_preview.short_description = "Image"

    def short_description(self, obj):
        if obj.bookDescription:
            return obj.bookDescription[:80] + "..." if len(obj.bookDescription) > 80 else obj.bookDescription
        return "-"

    short_description.short_description = "Description"