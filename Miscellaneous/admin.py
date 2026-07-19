from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from .models import Culture, History, Misecllaneous, Politics, Travel, Worldview


@admin.register(Misecllaneous)
class MisecllaneousAdmin(ModelAdmin):
    list_display = (
        "id",
        "misecllaneousTitle",
        "misecllaneousVideo",
        "misecllaneousCreateAt",
    )

    search_fields = (
        "misecllaneousTitle",
        "misecllaneousVideo",
    )

    list_filter = (
        "misecllaneousCreateAt",
    )

    ordering = ("-misecllaneousCreateAt",)

    list_per_page = 20

    readonly_fields = (
        "misecllaneousCreateAt",
    )

    fieldsets = (
        ("Miscellaneous Information", {
            "fields": (
                "misecllaneousTitle",
                "misecllaneousVideo",
            )
        }),
        ("Timestamp", {
            "fields": (
                "misecllaneousCreateAt",
            )
        }),
    )


class MiscellaneousContentAdmin(ModelAdmin):
    list_display = (
        "id",
        "content_image_preview",
        "contentName",
        "contentAuthor",
        "contentCreateAt",
    )
    search_fields = (
        "contentName",
        "contentAuthor",
        "contentDescription",
    )
    list_filter = ("contentCreateAt",)
    ordering = ("-contentCreateAt",)
    list_per_page = 20
    readonly_fields = ("contentCreateAt", "contentUpdateAt")
    fieldsets = (
        (
            "Content Information",
            {
                "fields": (
                    "contentImg",
                    "contentName",
                    "contentAuthor",
                    "contentDescription",
                )
            },
        ),
        (
            "Timestamps",
            {"fields": ("contentCreateAt", "contentUpdateAt")},
        ),
    )

    @admin.display(description="Content Image")
    def content_image_preview(self, obj):
        if not obj.contentImg:
            return "-"

        return format_html(
            '<img src="{}" width="60" height="60" '
            'style="border-radius:6px; object-fit:cover;" />',
            obj.contentImg,
        )


admin.site.register(Culture, MiscellaneousContentAdmin)
admin.site.register(Travel, MiscellaneousContentAdmin)
admin.site.register(History, MiscellaneousContentAdmin)
admin.site.register(Politics, MiscellaneousContentAdmin)
admin.site.register(Worldview, MiscellaneousContentAdmin)
