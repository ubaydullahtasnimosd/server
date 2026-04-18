from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Misecllaneous


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