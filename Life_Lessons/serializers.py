from rest_framework import serializers

from .models import Life_Lessons


class LifeLessonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Life_Lessons
        fields = [
            "id",
            "lifeLessonImg",
            "lifeLessonName",
            "lifeLessonAuthor",
            "lifeLessonDescription",
            "lifeLessonCreateAt",
            "lifeLessonUpdateAt",
        ]
        read_only_fields = [
            "id",
            "lifeLessonCreateAt",
            "lifeLessonUpdateAt",
        ]

