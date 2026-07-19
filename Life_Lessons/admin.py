from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from .models import Life_Lessons


@admin.register(Life_Lessons)
class LifeLessonsAdmin(ModelAdmin):
    list_display = (
        "id",
        "lesson_image_preview",
        "lifeLessonName",
        "lifeLessonAuthor",
        "lifeLessonCreateAt",
    )
    search_fields = (
        "lifeLessonName",
        "lifeLessonAuthor",
        "lifeLessonDescription",
    )
    list_filter = ("lifeLessonCreateAt",)
    ordering = ("-lifeLessonCreateAt",)
    list_per_page = 20
    readonly_fields = (
        "lifeLessonCreateAt",
        "lifeLessonUpdateAt",
    )
    fieldsets = (
        (
            "Lesson Information",
            {
                "fields": (
                    "lifeLessonImg",
                    "lifeLessonName",
                    "lifeLessonAuthor",
                    "lifeLessonDescription",
                )
            },
        ),
        (
            "Timestamps",
            {"fields": ("lifeLessonCreateAt", "lifeLessonUpdateAt")},
        ),
    )

    @admin.display(description="Lesson Image")
    def lesson_image_preview(self, obj):
        if not obj.lifeLessonImg:
            return "-"

        return format_html(
            '<img src="{}" width="60" height="60" '
            'style="border-radius:6px; object-fit:cover;" />',
            obj.lifeLessonImg,
        )

