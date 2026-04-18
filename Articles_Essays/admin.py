from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from .models import Articles_Essays


def get_image_url(image_field):
    if not image_field:
        return None
    try:
        return image_field.url
    except AttributeError:
        return image_field


@admin.register(Articles_Essays)
class ArticlesEssaysAdmin(ModelAdmin):
    list_display = (
        "id",
        "article_image_preview",
        "articlesEssaysName",
        "articlesEssaysAuthor",
        "qr_image_preview",
        "articlesEssaysQRCodeScen",
        "articlesEssaysCreateAt",
    )

    search_fields = (
        "articlesEssaysName",
        "articlesEssaysAuthor",
        "articlesEssaysDescription",
        "articlesEssaysQRCodeScen",
    )

    list_filter = (
        "articlesEssaysCreateAt",
    )

    ordering = ("-articlesEssaysCreateAt",)

    list_per_page = 20

    readonly_fields = (
        "articlesEssaysCreateAt",
        "articlesEssaysUpdateAt",
    )

    fieldsets = (
        ("Article Information", {
            "fields": (
                "articlesEssaysImg",
                "articlesEssaysName",
                "articlesEssaysAuthor",
                "articlesEssaysDescription",
            )
        }),
        ("QR Code Information", {
            "fields": (
                "articlesEssaysQRCodeScen",
                "articlesEssaysQRCodeScenImg",
            )
        }),
        ("Timestamps", {
            "fields": (
                "articlesEssaysCreateAt",
                "articlesEssaysUpdateAt",
            )
        }),
    )

    def article_image_preview(self, obj):
        image_url = get_image_url(obj.articlesEssaysImg)
        if not image_url:
            return "-"
        return format_html(
            '<img src="{}" width="60" height="60" style="border-radius:6px; object-fit:cover;" />',
            image_url
        )

    article_image_preview.short_description = "Article Image"

    def qr_image_preview(self, obj):
        image_url = get_image_url(obj.articlesEssaysQRCodeScenImg)
        if not image_url:
            return "-"
        return format_html(
            '<img src="{}" width="60" height="60" style="border-radius:6px; object-fit:cover;" />',
            image_url
        )

    qr_image_preview.short_description = "QR Image"