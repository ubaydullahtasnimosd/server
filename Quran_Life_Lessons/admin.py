from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from .models import Quran_Life_Lessons

def get_image_url(image_field):
    if not image_field:
        return None
    try:
        return image_field.url
    except AttributeError:
        return image_field

@admin.register(Quran_Life_Lessons)
class QuranLifeLessonsAdmin(ModelAdmin):
    list_display = (
        "id",
        "lesson_image_preview",
        "quranLessonName",
        "quranLessonAuthor",
        "quranLessonCreateAt",
    )

    search_fields = (
        "quranLessonName",
        "quranLessonAuthor",
        "quranLessonDescription",
    )

    list_filter = (
        "quranLessonCreateAt",
    )

    ordering = ("-quranLessonCreateAt",)

    list_per_page = 20

    readonly_fields = (
        "quranLessonCreateAt",
        "quranLessonUpdateAt",
    )

    fieldsets = (
        ("Lesson Information", {
            "fields": (
                "quranLessonImg",
                "quranLessonName",
                "quranLessonAuthor",
                "quranLessonDescription",
            )
        }),
        ("Timestamps", {
            "fields": (
                "quranLessonCreateAt",
                "quranLessonUpdateAt",
            )
        }),
    )

    def lesson_image_preview(self, obj):
        image_url = get_image_url(obj.quranLessonImg)
        if not image_url:
            return "-"
        return format_html(
            '<img src="{}" width="60" height="60" style="border-radius:6px; object-fit:cover;" />',
            image_url
        )

    lesson_image_preview.short_description = "Lesson Image"
