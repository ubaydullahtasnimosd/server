from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Visitor


@admin.register(Visitor)
class VisitorAdmin(ModelAdmin):
    list_display = (
        "id",
        "count",
    )

    ordering = ("-id",)

    list_per_page = 20

    fieldsets = (
        ("Visitor Information", {
            "fields": (
                "count",
            )
        }),
    )