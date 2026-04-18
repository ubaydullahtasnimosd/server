from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from .models import Readers_Love_Img, Readers_Love


def get_image_url(image_field):
    if not image_field:
        return None
    try:
        return image_field.url
    except AttributeError:
        return image_field


@admin.register(Readers_Love)
class ReadersLoveAdmin(ModelAdmin):
    list_display = (
        "id",
        "readersBookName",
        "readersName",
        "short_review",
        "readersReviewCreated",
    )

    search_fields = (
        "readersBookName",
        "readersName",
        "readersReview",
    )

    list_filter = (
        "readersReviewCreated",
    )

    ordering = ("-readersReviewCreated",)

    list_per_page = 20

    readonly_fields = (
        "readersReviewCreated",
    )

    fieldsets = (
        ("Reader Review Information", {
            "fields": (
                "readersBookName",
                "readersName",
                "readersReview",
            )
        }),
        ("Timestamp", {
            "fields": (
                "readersReviewCreated",
            )
        }),
    )

    def short_review(self, obj):
        if obj.readersReview:
            return obj.readersReview[:80] + "..." if len(obj.readersReview) > 80 else obj.readersReview
        return "-"

    short_review.short_description = "Review"


@admin.register(Readers_Love_Img)
class ReadersLoveImgAdmin(ModelAdmin):
    list_display = (
        "id",
        "image_preview",
        "readersReviewCreated",
    )

    list_filter = (
        "readersReviewCreated",
    )

    ordering = ("-readersReviewCreated",)

    list_per_page = 20

    readonly_fields = (
        "readersReviewCreated",
    )

    fieldsets = (
        ("Image Information", {
            "fields": (
                "readersBookImg",
            )
        }),
        ("Timestamp", {
            "fields": (
                "readersReviewCreated",
            )
        }),
    )

    def image_preview(self, obj):
        image_url = get_image_url(obj.readersBookImg)
        if not image_url:
            return "-"
        return format_html(
            '<img src="{}" width="60" height="60" style="border-radius:6px; object-fit:cover;" />',
            image_url
        )

    image_preview.short_description = "Image"