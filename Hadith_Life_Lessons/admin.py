from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from .models import Hadith_Life_Lessons


@admin.register(Hadith_Life_Lessons)
class HadithLifeLessonsAdmin(ModelAdmin):
    list_display = (
        "id",
        "lesson_image_preview",
        "hadithLessonName",
        "hadithLessonAuthor",
        "hadithLessonCreateAt",
    )
    search_fields = (
        "hadithLessonName",
        "hadithLessonAuthor",
        "hadithLessonDescription",
    )
    list_filter = ("hadithLessonCreateAt",)
    ordering = ("-hadithLessonCreateAt",)
    list_per_page = 20
    readonly_fields = (
        "hadithLessonCreateAt",
        "hadithLessonUpdateAt",
    )
    fieldsets = (
        (
            "Lesson Information",
            {
                "fields": (
                    "hadithLessonImg",
                    "hadithLessonName",
                    "hadithLessonAuthor",
                    "hadithLessonDescription",
                )
            },
        ),
        (
            "Timestamps",
            {"fields": ("hadithLessonCreateAt", "hadithLessonUpdateAt")},
        ),
    )

    @admin.display(description="Lesson Image")
    def lesson_image_preview(self, obj):
        if not obj.hadithLessonImg:
            return "-"

        return format_html(
            '<img src="{}" width="60" height="60" '
            'style="border-radius:6px; object-fit:cover;" />',
            obj.hadithLessonImg,
        )

