from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from .models import AboutAuthor


def get_image_url(image_field):
    if not image_field:
        return None
    try:
        return image_field.url
    except AttributeError:
        return image_field


@admin.register(AboutAuthor)
class AboutAuthorAdmin(ModelAdmin):
    list_display = (
        "id",
        "image_preview",
        "aboutAuthorName",
        "short_description",
    )

    search_fields = (
        "aboutAuthorName",
        "aboutAuthorDescription",
    )

    ordering = ("-id",)

    list_per_page = 20

    fieldsets = (
        ("Author Information", {
            "fields": (
                "aboutAuthorImg",
                "aboutAuthorName",
                "aboutAuthorDescription",
            )
        }),
    )

    def image_preview(self, obj):
        image_url = get_image_url(obj.aboutAuthorImg)
        if not image_url:
            return "-"
        return format_html(
            '<img src="{}" width="60" height="60" style="border-radius:6px; object-fit:cover;" />',
            image_url
        )

    image_preview.short_description = "Image"

    def short_description(self, obj):
        if obj.aboutAuthorDescription:
            return obj.aboutAuthorDescription[:80] + "..." if len(obj.aboutAuthorDescription) > 80 else obj.aboutAuthorDescription
        return "-"

    short_description.short_description = "Description"